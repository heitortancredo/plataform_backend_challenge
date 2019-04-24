from app import create_app

application = create_app('config.cfg')
# application = create_app('test.cfg')

if __name__ == '__main__':
        application.run()
