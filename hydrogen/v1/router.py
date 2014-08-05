#!/bin/python
import wsgi
import svtest.routers
import svtest2.routers
import svmanmod.routers
import auths.routers
from hydrogen.svmodproxy import routers as svmodproxy_routers
from hydrogen.tcdbproxy import routers as tcdbproxy_routers
class ControllerTest(object):
    def __init__(self):
        print "ControllerTest!!!!"
    def test(self,req):
          print "req",req
          return {
            'name': "test",
            'properties': "test"
        }

class MyRouterApp(wsgi.Router):
      '''
      app
      '''
      def __init__(self,mapper):
          controller = ControllerTest()
          mapper.connect('/test',
                       controller=wsgi.Resource(controller),
                       action='test',
                       conditions={'method': ['GET']})
          super(MyRouterApp, self).__init__(mapper)

#@fail_gracefully
def auth_app_factory(global_conf, **local_conf):
    #controllers.register_version('v2.0')
    #conf = global_conf.copy()
    #conf.update(local_conf)
    return wsgi.ComposingRouter(wsgi.APIMapper(),
                               [#svtest.routers.Public(),
                                #svtest2.routers.SV2Public(),
                                #svmanmod.routers.Public()
                                svmodproxy_routers.Public(),
                                tcdbproxy_routers.Public()
                                ])
                               #token.routers.Router(),
                               #routers.VersionV2('public'),
                               #routers.Extension(False)])
def public_app_factory(global_conf,**local_conf):
    return wsgi.ComposingRouter(wsgi.APIMapper(),
                                [auths.routers.Public()])
