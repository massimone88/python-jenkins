import xml.etree.ElementTree
__author__ = 'massimone88 <stefano.mandruzzato@gmail.com>'
__version__ = '1.0.0'

class CleanWorkSpaceService(object):
    @staticmethod
    def _add_post_build(job_config, postBuildElem):
        root = xml.etree.ElementTree.ElementTree(xml.etree.ElementTree.fromstring(job_config)).getroot()
        publisherElem = root.find('./publishers')
        publisherElem.append(postBuildElem)
        xmlstr = xml.etree.ElementTree.tostring(root, encoding='utf8', method='xml')
        return xmlstr

    @staticmethod
    def _retrieve_exclude_pattern_clean_workspace(job_config):
        root = xml.etree.ElementTree.ElementTree(xml.etree.ElementTree.fromstring(job_config)).getroot()
        preBluildCleanUpElem = root.find('./buildWrappers/hudson.plugins.ws__cleanup.PreBuildCleanup')
        patternsElem = preBluildCleanUpElem.findall('patterns/hudson.plugins.ws__cleanup.Pattern')
        patterns = []
        for patternElem in patternsElem:
            patterns.append(patternElem.find('pattern').text)

        print "exclude_patterns %s" % patterns
        return patterns

    @staticmethod
    def _create_post_build_clean_workspace(exclude_patterns):
        post_clean_workspace_elem = xml.etree.ElementTree.Element('hudson.plugins.ws__cleanup.WsCleanup')
        post_clean_workspace_elem.set('plugin', 'ws-cleanup@0.32')
        subElem = xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'patterns')
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'deleteDirs').text = 'true'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'skipWhenFailed').text = 'false'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanWhenSuccess').text = 'true'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanWhenUnstable').text = 'true'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanWhenFailure').text = 'false'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanWhenNotBuilt').text = 'true'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanWhenAborted').text = 'true'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'notFailBuild').text = 'false'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'cleanupMatrixParent').text = 'false'
        xml.etree.ElementTree.SubElement(post_clean_workspace_elem, 'externalDelete')
        for patterns in exclude_patterns:
            pattern_elem = xml.etree.ElementTree.SubElement(subElem, 'hudson.plugins.ws__cleanup.Pattern')
            xml.etree.ElementTree.SubElement(pattern_elem, 'pattern').text = patterns
            xml.etree.ElementTree.SubElement(pattern_elem, 'type').text = 'EXCLUDE'
        return post_clean_workspace_elem

    @staticmethod
    def add_post_build_clean_workspace(job_config):
        exclude_patterns = CleanWorkSpaceService._retrieve_exclude_pattern_clean_workspace(job_config)
        postBuildElem = CleanWorkSpaceService._create_post_build_clean_workspace(exclude_patterns)
        return CleanWorkSpaceService._add_post_build(job_config, postBuildElem)
