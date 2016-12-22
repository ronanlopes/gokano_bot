#-*- coding: utf-8 -*-

import os
import sys
import resource

def create_daemon(stdout, stderr, working_dir):
    """
    cria um daemon
    """
    # faz o primeiro fork
    _fork_off_and_die()
    # cria uma nova sessão 
    os.setsid()
    # faz o segundo fork
    _fork_off_and_die()
    # altera a máscara de arquivos
    os.umask(0)
    # altera o diretório de trabalho
    os.chdir(working_dir)
    # fecha todos os descritores de arquivos
    _close_file_descriptors()
    # redireciona stdout e stderr
    _redirect_file_descriptors(stdout, stderr)

def _fork_off_and_die():    
    """
    cria um fork e sai do processo pai
    """
    pid = os.fork()
    # se o pid == 0, é o processo filho
    # se o pid > é o processo pai
    if pid != 0:
        sys.exit(0)

def _close_file_descriptors():
    # Fechando todos os file descriptors para evitar algum
    # lock

    # RLIMIT_NOFILE é o número de descritores de arquivo que
    # um processo pode manter aberto
    limit = resource.getrlimit(resource.RLIMIT_NOFILE)[1]
    for fd in range(limit):
        try:
            os.close(fd)
        except OSError:
            pass

def _redirect_file_descriptors(stdout, stderr):
    """
    redireciona stdout e stderr 
    """
    # redirecionando stdout e stderr
    for fd in sys.stdout, sys.stderr:
        fd.flush()

    sys.stdout= open(stdout, 'a', 1)
    sys.stderr = open(stderr, 'a', 1)

def daemonize_func(func, stdout, stderr, working_dir, *args, **kwargs):
    """
    executa uma função como um daemon
    """
    create_daemon(stdout, stderr, working_dir)
    func(*args, **kwargs)

class daemonize(object):
    """
    decorator para executar uma função como daemon
    """

    def __init__(self, stdout='/dev/null/', stderr='/dev/null/',
                 working_dir='.'):

        # stdout e stderr são os lugares para onde serão redirecionados
        # sys.stdout e sys.stderr
        self.stdout = stdout
        self.stderr = stderr
        # working_dir é o diretório onde o daemon trabalhará
        self.working_dir = working_dir

    def __call__(self, func):
        def decorated_function(*args, **kwargs):
            daemonize_func(func, self.stdout, self.stderr, self.working_dir,
                      *args, **kwargs)
        return decorated_function