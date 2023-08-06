import logging
import sys
import os
import jsonschema
import re
import yaml

from pathlib import Path

from spaceone.core.service import *
from spaceone.core import utils
from spaceone.core import config

from spaceone.repository.error import *
from spaceone.repository.model.capability_model import Capability
from spaceone.repository.manager.identity_manager import IdentityManager
from spaceone.repository.manager.plugin_manager.local_plugin_manager import LocalPluginManager
from spaceone.repository.manager.plugin_manager.managed_plugin_manager import ManagedPluginManager
from spaceone.repository.manager.plugin_manager.remote_plugin_manager import RemotePluginManager
from spaceone.repository.manager.repository_manager import RepositoryManager

_LOGGER = logging.getLogger(__name__)

MAX_IMAGE_NAME_LENGTH = 48
REGISTRY_MAP = {
        "DOCKER_HUB": "DockerHubConnector",
        "AWS_PUBLIC_ECR": "AWSPublicECRConnector",
        "HARBOR": "HarborConnector"
        }

def _load_yaml_data(file_path):
	try:
		# Load YAML data from the file
		with open(file_path, 'r') as file:
			yaml_data = yaml.safe_load(file)

		# Access and process the loaded YAML data
		# Example: Printing the loaded data
		return yaml_data

	except FileNotFoundError:
		_LOGGER.error(f"File '{file_path}' not found.")
		return False

	except yaml.YAMLError as e:
		_LOGGER.error(f"Error loading YAML file: {e}")
		return False

@authentication_handler(exclude=['get', 'get_versions'])
@authorization_handler(exclude=['get', 'get_versions'])
@mutation_handler
@event_handler
class PluginService(BaseService):

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['name', 'service_type', 'image', 'domain_id'])
    def register(self, params):
        """Register Plugin (local repo only)

        Args:
            params (dict): {
                'name': 'str',
                'service_type': 'str',
                'registry_type': 'str',
                'registry_config': 'dict',
                'image': 'str',
                'provider': 'str',
                'capability': 'dict',
                'template': 'dict',
                'labels': 'list',
                'tags': 'dict',
                'project_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            plugin_vo (object)
        """

        registry_type = params.get('registry_type', 'DOCKER_HUB')
        registry_config = params.get('registry_config', {})

        # Pre-condition Check
        self._check_template(params.get('template'))
        # self._check_capability(params.get('capability'))
        self._check_project(params.get('project_id'), params['domain_id'])
        self._check_service_type(params.get('service_type'))
        self._check_image(params['image'])
        self._check_registry_type(registry_type)
        self._check_registry_config(registry_type, registry_config)

        plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager')
        # update image_prefix, if exist (harbor case)
        
        # Only LOCAL repository can be registered
        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        params['plugin_id'] = self._check_plugin_naming_rules(params['image'])
        params['repository'] = repo_mgr.get_local_repository()
        params['repository_id'] = params['repository'].repository_id

        plugin_vo = plugin_mgr.register_plugin(params)

        versions = plugin_mgr.get_plugin_versions(plugin_vo.plugin_id, plugin_vo.domain_id)

        if len(versions) == 0:
            raise ERROR_NO_IMAGE_IN_REGISTRY(registry_type=plugin_vo.registry_type, image=plugin_vo.image)

        return plugin_vo

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id', 'domain_id'])
    def update(self, params):
        """Update Plugin. (local repo only)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'name': 'str',
                'capability': 'dict',
                'template': 'dict',
                'labels': 'list',
                'tags': 'dict'
                'domain_id': 'str'
            }

        Returns:
            plugin_vo (object)
        """

        # Pre-condition Check
        self._check_template(params.get('template'))
        # self._check_capability(params.get('capability'))
        self._check_service_type(params.get('service_type'))

        plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager')
        return plugin_mgr.update_plugin(params)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id', 'domain_id'])
    def deregister(self, params):
        """Deregister Plugin (local repo only)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            plugin_vo (object)
        """
        plugin_id = params['plugin_id']
        domain_id = params['domain_id']

        #########################################################################
        # Warning 
        #
        # To deregister plugin, plugin has to verify there is no installed plugins
        # If there was installed plugin, other micro service can query endpoint
        # But plugin can not reply endpoint
        ##########################################################################
        # TODO: check plugin is not used

        plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager')
        return plugin_mgr.delete_plugin(plugin_id, domain_id)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id', 'domain_id'])
    def enable(self, params):
        """ Enable plugin (local repo only)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            plugin_vo (object)
        """
        plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager')
        return plugin_mgr.enable_plugin(params['plugin_id'], params['domain_id'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id', 'domain_id'])
    def disable(self, params):
        """ Disable Plugin (local repo only)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            plugin_vo (object)
        """
        plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager')
        return plugin_mgr.disable_plugin(params['plugin_id'], params['domain_id'])

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id'])
    def get_versions(self, params):
        """ Get Plugin version (local & remote)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'repository_id': 'str',
                'domain_id': 'str'
            }

        Returns:
            version_list (list)
        """

        plugin_id = params['plugin_id']
        domain_id = params.get('domain_id')
        repo_id = params.get('repository_id')

        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        repo_vos = repo_mgr.get_all_repositories(repo_id)

        for repo_vo in repo_vos:
            plugin_mgr = self._get_plugin_manager_by_repo(repo_vo)
            try:
                _LOGGER.debug(f'[get_versions] find at name: {repo_vo.name} '
                              f'(repo_type: {repo_vo.repository_type})')
                version_list = plugin_mgr.get_plugin_versions(plugin_id, domain_id)
            except Exception as e:
                version_list = None

            if version_list is not None:
                return version_list

            # if version_list:
            #     _LOGGER.debug(f'[get_versions] version_list: {version_list}')
            #     # User wants reverse list
            #     try:
            #         sorted_version_list = sorted(version_list, key=LooseVersion, reverse=True)
            #     except Exception as e:
            #         _LOGGER.debug(f'[get_versions] loose sort failed: {e}')
            #         sorted_version_list = sorted(version_list, reverse=True)
            #     _LOGGER.debug(f'[get_versions] sorted version_list: {sorted_version_list}')
            #     return sorted_version_list

        _LOGGER.error(f'[get_versions] no version: {plugin_id}')
        raise ERROR_NO_PLUGIN(plugin_id=plugin_id)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['plugin_id'])
    @change_only_key({'repository_info': 'repository'})
    def get(self, params):
        """ Get Plugin (local & remote)

        Args:
            params (dict): {
                'plugin_id': 'str',
                'repository_id': 'str',
                'domain_id': 'str',
                'only': 'list'
            }

        Returns:
            plugin_vo (object)
        """
        plugin_id = params['plugin_id']
        domain_id = params.get('domain_id')
        repo_id = params.get('repository_id')
        only = params.get('only')

        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        repo_vos = repo_mgr.get_all_repositories(repo_id)

        for repo_vo in repo_vos:
            _LOGGER.debug(f'[get] find at name: {repo_vo.name} '
                          f'(repo_type: {repo_vo.repository_type})')
            plugin_mgr = self._get_plugin_manager_by_repo(repo_vo)
            try:
                plugin_vo = plugin_mgr.get_plugin(plugin_id, domain_id, only)
            except Exception as e:
                plugin_vo = None

            if plugin_vo:
                return plugin_vo

        raise ERROR_NO_PLUGIN(plugin_id=plugin_id)

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @change_only_key({'repository_info': 'repository'}, key_path='query.only')
    @append_query_filter(['repository_id', 'plugin_id', 'name', 'state', 'service_type',
                          'registry_type', 'provider', 'project_id', 'domain_id'])
    @append_keyword_filter(['plugin_id', 'name', 'provider', 'labels'])
    def list(self, params):
        """ List plugins (local or repo)

        Args:
            params (dict): {
                'repository_id': 'str',
                'plugin_id': 'str',
                'name': 'str',
                'state': 'str',
                'service_type': 'str',
                'registry_type': 'str',
                'provider': 'str',
                'project_id': 'str',
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.Query)'
            }

        Returns:
            plugins_vo (object)
            total_count
        """

        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        query = params.get('query', {})
        only = query.get('only', [])

        if 'registry_url' in only:
            only.remove('registry_url')

        if repository_id := params.get('repository_id'):
            repo_vo = repo_mgr.get_repository(repository_id)

            plugin_mgr = self._get_plugin_manager_by_repo(repo_vo)

            return plugin_mgr.list_plugins(query)
        else:
            repository_vos, total_count = repo_mgr.list_repositories({})

            all_plugin_vos = []
            plugin_total_count = 0
            for repository_vo in repository_vos:
                plugin_mgr = self._get_plugin_manager_by_repo(repository_vo)
                plugin_vos, total_count = plugin_mgr.list_plugins(query)
                all_plugin_vos += plugin_vos
                plugin_total_count += total_count

            return all_plugin_vos, plugin_total_count

    @transaction(append_meta={'authorization.scope': 'DOMAIN'})
    @check_required(['query', 'repository_id'])
    @append_query_filter(['repository_id', 'domain_id'])
    @append_keyword_filter(['plugin_id', 'name', 'provider', 'labels'])
    def stat(self, params):
        """
        Args:
            params (dict): {
                'domain_id': 'str',
                'query': 'dict (spaceone.api.core.v1.StatisticsQuery)'
            }

        Returns:
            values (list) : 'list of statistics data'

        """

        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        repository_id = params['repository_id']
        repo_vo = repo_mgr.get_repository(repository_id)

        plugin_mgr = self._get_plugin_manager_by_repo(repo_vo)
        query = params.get('query', {})
        return plugin_mgr.stat_plugins(query)

    def _get_plugin_manager_by_repo(self, repo_vo):
        if repo_vo.repository_type == 'local':
            local_plugin_mgr: LocalPluginManager = self.locator.get_manager('LocalPluginManager', repository=repo_vo)
            return local_plugin_mgr
        elif repo_vo.repository_type == 'managed':
            managed_plugin_mgr: ManagedPluginManager = self.locator.get_manager('ManagedPluginManager', repository=repo_vo)
            return managed_plugin_mgr
        else:
            remote_plugin_mgr: RemotePluginManager = self.locator.get_manager('RemotePluginManager', repository=repo_vo)
            return remote_plugin_mgr

    def create_managed_plugins(self, domain_id):
        # domain_id: root domain-id
        # find plugin contents
        # Get the path to the package data file
        dir_path = "/etc/cloudforet/plugin"
        directory = Path(dir_path)
        # Check for YAML files in the directory
        yaml_files = [item for item in directory.iterdir() if item.is_file() and item.suffix == '.yaml']

        # loop all plugin
        for yaml_file in yaml_files:
            data = _load_yaml_data(yaml_file)
            if data == False:
                # wrong yaml data (pass)
                continue
            self._create_managed_plugin(data, domain_id)
        # register
        pass

    def _create_managed_plugin(self, params, domain_id):
        plugin_mgr: ManagedPluginManager = self.locator.get_manager('ManagedPluginManager')
        # Only LOCAL repository can be registered
        repo_mgr: RepositoryManager = self.locator.get_manager('RepositoryManager')
        params["domain_id"] = domain_id
        params['plugin_id'] = self._check_plugin_naming_rules(params['image'])
        # TODO: change 
        params["registry_type"] = config.get_global("DEFAULT_REGISTRY", "DOCKER_HUB")
        params["registry_config"] = self._get_registry_config_from_settings(params["registry_type"])
        params['repository'] = repo_mgr.get_managed_repository()
        params['repository_id'] = params['repository'].repository_id

        # if prefix  exist
        image_prefix = self._get_image_prefix(params["registry_config"])
        if image_prefix:
            image = params["image"]
            params["image"] = f"{image_prefix}/{image}"
            # ex. my_company/my_harbor/my_cmp/spaceone/plugin-aws-ec2-inven-collector

        plugin_vo = plugin_mgr.register_plugin(params)

        #versions = plugin_mgr.get_plugin_versions(plugin_vo.plugin_id, plugin_vo.domain_id)

        #if len(versions) == 0:
        #    raise ERROR_NO_IMAGE_IN_REGISTRY(registry_type=plugin_vo.registry_type, image=plugin_vo.image)

        return plugin_vo

    def _get_registry_config_from_settings(self, registry_type):
        """ if there is no registry_config from parameter
        We automatically update by settings file
        """
        reg_dict = config.get_global("CONNECTORS", {})
        my_kind = REGISTRY_MAP[registry_type]
        my_data = reg_dict.get(my_kind, {})
        return my_data

    def _get_image_prefix(self, registry_config):
        """ example: my_company/my_harbor/_my_cmp
        """
        image_prefix = registry_config.get("image_prefix", None)
        return image_prefix

    @staticmethod
    def _check_template(template):
        """
        Check json schema
        """
        if template:
            for key, value in template.items():
                if isinstance(value, dict) and 'schema' in value:
                    try:
                        jsonschema.Draft7Validator.check_schema(value['schema'])
                    except Exception as e:
                        raise ERROR_INVALID_TEMPLATE_SCHEMA(key=f'template.{key}')

    @staticmethod
    def _check_capability(capability):
        if capability:
            try:
                capability_vo = Capability(capability)
                capability_vo.validate()
            except Exception as e:
                raise ERROR_INVALID_PARAMETER(key='capability', reason=e)

    @staticmethod
    def _check_service_type(name):
        """
        service_type has format rule
        format:
            <service>.<purpose>
        example:
            identity.domain
            inventory.collector

        Raises:
            ERROR_INVALID_PARAMETER
        """
        if name:
            pass
            # idx = name.split('.')
            # if len(idx) != 2:
            #     raise ERROR_INVALID_PARAMETER(key='service_type', reason=f'{name} format is invalid.')

    def _check_project(self, project_id, domain_id):
        if project_id:
            identity_mgr: IdentityManager = self.locator.get_manager('IdentityManager')
            identity_mgr.get_project(project_id, domain_id)

    @staticmethod
    def _check_plugin_naming_rules(image):
        """ Check plugin name conventions

        Rules:
          - no space
        """
        parsed_items = image.split('/')
        checked_name = parsed_items[-1]

        return checked_name

    @staticmethod
    def _check_registry_type(registry_type):
        registry_url = config.get_global('REGISTRY_URL_MAP', {}).get(registry_type)

        if registry_url.strip() == '':
            raise ERROR_REGISTRY_SETTINGS(registry_type=registry_type)

    @staticmethod
    def _check_registry_config(registry_type, registry_config):
        if registry_type == 'AWS_PUBLIC_ECR':
            if 'account_id' not in registry_config:
                raise ERROR_REQUIRED_PARAMETER(key='registry_config.account_id')

    @staticmethod
    def _check_image(name):
        """ Check image name
        format: repository/image_name
        length of image_name: < 40
        format of image_name: string and - (underscore is not allowed)
        """
        _LOGGER.debug(f'[_check_image] {name}')
        items = name.split('/')
        size = len(items)
        if size == 1:
            # Not repository
            image_name = items[0]
        elif size == 2:
            repo = items[0]
            image_name = items[1]
        elif size == 3:
            alias = items[0]
            alias = items[1]
            image_name = items[2]
        else:
            # wrong format
            raise ERROR_INVALID_IMAGE_FORMAT(name=name)

        # check image_name
        image_len = len(image_name)
        if image_len > MAX_IMAGE_NAME_LENGTH:
            raise ERROR_INVALID_IMAGE_LENGTH(name=image_name, length=MAX_IMAGE_NAME_LENGTH)

        # Search naming format
        m = re.search('(?![a-zA-Z0-9\-]).*', image_name)
        if m:
            if len(m.group()) > 1:
                raise ERROR_INVALID_IMAGE_NAME_FORMAT(name=image_name)
            return True
        raise ERROR_INVALID_IMAGE_NAME_FORMAT(name=image_name)
