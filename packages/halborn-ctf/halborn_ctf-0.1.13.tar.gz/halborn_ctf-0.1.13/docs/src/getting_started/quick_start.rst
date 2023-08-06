.. _quick_start:

Quick Start
===========

Following sections provide a - little talk, much code - introduction to ``halborn-ctf``.
Everything should be copy-pastable and work out of the box, given your
:ref:`installation` was successful.

.. contents::
   :local:

Requirements
---------------------------

- ``halborn_ctf``
- ``docker``


Initializing the challenge
---------------------------

Over an empty folder type the following command:

.. code-block:: console

    $ halborn_ctf init

.. code-block:: console

    $ cat Dockefile

.. code::

    FROM python:3.11.2

    RUN pip install halborn_ctf==0.1.11

    # Your dependencies

    COPY Dockerfile .
    COPY challenge.py .

    # Your build commands

    RUN halborn_ctf build --local

    ENTRYPOINT ["halborn_ctf"]
    CMD ["local"]

.. code-block:: console

    $ cat challenge.py

.. code::

    from halborn_ctf.templates import GenericChallenge

    class Challenge(GenericChallenge):

        HAS_SOLVER = True

        CHALLENGE_NAME = 'MY CHALLENGE'

        def run(self):
            # Do deployment
            pass

        def solver(self):
            self.solved = True


Check that the challenge can build, this will compile the ``Dockerfile`` into a local image:

.. code-block:: console

    $ halborn_ctf build

Check that the challenge can run (:mod:`halborn_ctf.templates.GenericChallenge.run`). This will run  the build
image and expose the required ports:

.. code-block:: console

    $ halborn_ctf run -vvv

    2023-06-17 16:05:58 | halborn_ctf.cli | main | WARNING | ============================
    2023-06-17 16:05:58 | halborn_ctf.cli | main | WARNING | Logging level: DEBUG
    2023-06-17 16:05:58 | halborn_ctf.cli | main | WARNING | ============================
    2023-06-17 16:05:58 | root | __enter__ | INFO | pid=1  pgid=1
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:8080
    * Running on http://172.17.0.3:8080


You should see that a server has been spawned locally on port ``8080``.

By default the challenge will expose the following routes:

- ``/info``: Does return challenge public state: ``{"ready":true,"state":{},"config":{}}`` (http://127.0.0.1:8080/info)


.. note::
    Since we have set ``HAS_SOLVER`` (:mod:`halborn_ctf.templates.GenericChallenge.HAS_SOLVER`). The ``solver`` function must exist.
    The ``/solved`` route will also be exposed (http://127.0.0.1:8080/solved). Each time the route is accessed this function will be executed before responding the HTTP request.

    The route is now returning that the challenge is solved as we set ``self.solved = True``::

        {
            "msg": "Solved",
            "solved": true
        }

.. tip::
    If the function does take a lot to execute or does require background processing take a look at :ref:`periodic-solver`.


.. tip::
    If you have all the dependencies on your local system and want to play the challenge locally you can always use:

    .. code-block:: console

        $ halborn_ctf local -vvv

Creating the challenge
----------------------

You can now modify the template files to meat your challenge requirements. Keep in mind that everything inside
the (:mod:`halborn_ctf.templates.GenericChallenge.run`) function will be executed for every new challenge instance. This means that long process
actions should be included on the ``Dockerfile`` instead. The build phase will be caching all layers and speedup development.


Service mapping
---------------

The previous code does have the minimum required functions to run a challenge. However, it does not have any functionallity and there is no way to access services. To register
internal services and expose them on the challenge server you must define a path mapping attribute (:mod:`halborn_ctf.templates.GenericChallenge.PATH_MAPPING`):


.. code::

    from halborn_ctf.templates import GenericChallenge

    import halborn_ctf.shell as shell
    import halborn_ctf.network as network

    import requests

    class Challenge(GenericChallenge):

        HAS_SOLVER = True

        CHALLENGE_NAME = 'MY CHALLENGE'

        # rule1: A request to http://challenge/ will be proxied to http://127.0.0.1:9999/.
        # rule2: A request to http://challenge/my_path/file will be proxied to http://127.0.0.1:9999/my_path/file.

        PATH_MAPPING = {
            '/': {
                'port': 9999,
                'path': '/',
                'methods': ['GET']
            },
            '/<path:path>': {
                'port': 9999,
                'path': '/',
                'methods': ['GET']
            }
        }

        def run(self):
            # Do deployment
            shell.run('python -m http.server 9999', background=True)
            network.wait_for_port(9999)

        def solver(self):
            response = requests.get('http://127.0.0.1:9999')
            if "halborn_ctf.txt" in response:
                self.solved = True

The previous challenge does use functions from this framework to run a shell command in the background with an http
server on the current directory. It then waits for the port to be listening.

If you now try to access http://127.0.0.1:8080 you will be able to see the current directory listing. This is achieved by the ``PATH_MAPPING`` attribute which proxies
any request on the ``/`` path to the server listening on port ``9999``. It also proxies any subpath request ``/<path:path>`` to the same server from the ``/`` path.

If you now try to request http://127.0.0.1:8080/solved you will see that the challenge does report as not being solved.

.. tip::

    To solve the challenge create a file named ``halborn_ctf.txt`` under the challenge directory:

    .. code-block:: console

        $ touch halborn_ctf.txt



Downloadable files
------------------


Some challenges require the players to have some files to be used. For that the ``HAS_FILES`` (:mod:`halborn_ctf.templates.GenericChallenge.HAS_FILES`) flag can be set to ``True``. Doing so, a function named ``files`` should be declared.

We can create a file as a test to be exposed with the challenge:


.. code-block:: console

    $ echo "Test content" > test.txt

.. code::

    from halborn_ctf.templates import GenericChallenge

    class Challenge(GenericChallenge):

        HAS_SOLVER = True
        HAS_FILES = True

        CHALLENGE_NAME = 'MY CHALLENGE'

        def run(self):
            # Do deployment....
            pass

        def solver(self):
            self.solved = True

        def files(self):
            return [
                'test.txt'
            ]


If we now try to access the server at ``/files`` (http://127.0.0.1:8080/files) a ``MY_CHALLENGE.zip`` file will be downloaded. The name is taken from ``CHALLENGE_NAME``. The content of the file should include the ``test.txt`` and the ``challenge.py`` file itself.

Working with the state
----------------------

If you want to persist variables across ``build`` and ``run`` and all periodic functions
you can use the :obj:`halborn_ctf.templates.GenericChallenge.state` and :obj:`halborn_ctf.templates.GenericChallenge.state_public`
properties. This property can be accessed anywhere but must be declared on the ``__init__`` function with the initial values.


.. code::

    from halborn_ctf.templates import GenericChallenge

    class Challenge(GenericChallenge):

        HAS_SOLVER = True
        HAS_FILES = True

        CHALLENGE_NAME = 'MY CHALLENGE'

        def __init__(self):
            super().__init__()

            self.state = {
                'solved_attempts': 0
            }

        def run(self):
            # Do deployment
            pass

        def solver(self):
            self.state.solved_attempts += 1

            if self.state.solved_attempts == 2:
                self.solved = True

        def files(self):
            return [
                'test.txt'
            ]


.. note::
    The ``state_public`` can be accessed and seen on the ``/info`` challenge route. (http://127.0.0.1:8080/info)

.. _periodic-solver:

Periodic solver
---------------

If the function does take a lot to execute or does require background processing you can always define a periodic function and start it before setting the challenge to ready. Take a look on how to use the decorator under :obj:`halborn_ctf.functions.periodic`.

.. code::

    from halborn_ctf.templates import GenericChallenge

    from halborn_ctf.functions import periodic

    class Challenge(GenericChallenge):

        HAS_SOLVER = True

        CHALLENGE_NAME = 'MY CHALLENGE'

        @periodic(every=1)
        def my_checker(self):
            self.log.info('Checking...')

            # Do some long computation
            # ...
            # self.solved = True

            if self.solved:
                ########### Stop the periodic function ##########
                self.my_checker.stop()

        def run(self):
            # Do deployment

            ########### Start the periodic function ##########
            self.my_checker()

        def solver(self):
            # The solve is done on the `my_checker` function
            pass


The previous challenge will be logging the ``Checking...`` string on the console every 1 second.

.. warning::
    Although an external or periodic function is setting the ``self.solved`` the ``solver`` function must exist.