from flask_restx import Api

restX_api = Api(version='1,0',
                title='FPSO Equipment Manager',
                description='Backend to manage different equipment of an FPSO '
                            '(Floating Production, Storage and Offloading)')
