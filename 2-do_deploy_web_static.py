#!/usr/bin/python3
# Deploys source code to server
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['18.207.233.152', '100.26.221.176']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """

    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        fname = filename.split('.')[0]

        put(archive_path, f'/tmp/{filename}')
        run(f'mkdir -p /data/web_static/releases/{fname}/')
        run(f'tar -xzf /tmp/{filename} -C/data/web_static/releases/{fname}/')
        run(f'rm /tmp/{filename}')
        run(
            f'mv /data/web_static/releases/{fname}/web_static/*\
                    /data/web_static/releases/{fname}/'
        )
        run(f'rm -rf /data/web_static/releases/{fname}/web_static')
        run('rm -rf /data/web_static/current')
        run(f'ln -s /data/web_static/releases/{fname}\
                //data/web_static/current')

        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', e)
        return False
