# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deqr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deqr',
    'version': '0.2.2',
    'description': 'qr code decoding library',
    'long_description': "## deqr\n\nA python library for decoding QR codes. Implemented as a cython wrapper around\ntwo different QR code decoding backends (quirc and qrdec).\n\n### Install\n\n```\npip install deqr\n```\n\n### [Documentation][documentation]\n\n[documentation]: https://torque.github.io/deqr-docs/latest-dev/\n\n## Changelog\n\n### [0.2.2] - 2023-06-17\n\n#### Added\n\n  - packaging: pre-built Python 3.11 wheels ([7980904b](https://github.com/torque/deqr/commit/7980904b97bbfee0446e4a11bff5183f77ed26b7))\n\n#### Fixed\n\n  - Adapt `pyproject.toml` to more recent poetry-core so that the source package should work again ([58a8c77b](https://github.com/torque/deqr/commit/58a8c77bfe34b3e8e3b42dc6a6c20be2b4105052))\n\n#### Changed\n\n  - Update quirc to v1.2 ([9918646d](https://github.com/torque/deqr/commit/9918646d61e2d9b71c3fc84604d5a6bec4af4c98))\n  - Build dependencies: update cython to 3.0.0b3 and poetry-core to >=1.6.0,<1.7.0 (poetry-core is pinned to a narrow version range to hopefully avoid future breakage) ([a625da32](https://github.com/torque/deqr/commit/a625da32e2b8823a2a1619dc603e264cc3e86470), [58a8c77b](https://github.com/torque/deqr/commit/58a8c77bfe34b3e8e3b42dc6a6c20be2b4105052))\n  - Don't package dependency source files into bdists ([2bc4a61f](https://github.com/torque/deqr/commit/2bc4a61f654f0c352fa843cfc7fd2ca5ac661e21))\n  - Linux binary packages are now built to the manylinux_2_28 standard due to the manylinux_2_24 container being deprecated ([9b6e42e6](https://github.com/torque/deqr/commit/9b6e42e658cbbb3c30e149ed0f01c97d3daf3960))\n\n#### Removed\n\n  - Remove use of poetry-dynamic-versioning from the build process. It's convenient, but too flaky. Maintaining the version information in two places is not an unbearable maintenance burden, and CI can check for this ([5ea9a83e](https://github.com/torque/deqr/commit/5ea9a83e4e141bdd1b804cf00b8425441c7d725a))\n\n### [0.2.1] - 2022-01-22\n\n#### Added\n\n  - packaging: distribute Python 3.10 wheels ([034f14b3](https://github.com/torque/deqr/commit/034f14b323103f12de2077e34133a08792e3876e))\n\n#### Fixed\n\n  - Fixed the sdist so that source-based installs work (note: this was later broken by a Poetry update) ([b84b3716](https://github.com/torque/deqr/commit/b84b371621db3c3f181bf2a0e53d54b93ffee3af))\n\n### [0.2.0] - 2021-06-28\n\n#### Added\n\n  - Documentation. Things are now more documented than ever before.\n\n#### Changed\n\n  - QRdecDecoder now produces bounding box corners in clockwise order.\n  - [BREAKING] Both decoders try to convert decoded data to reasonable types by default.\n\n#### Fixed\n\n  - binarize.binarze is now callable from Python code.\n  - Decoding codes from PIL and bytes objects now actually works.\n  - The sdist now contains the dependency code so it can be built.\n  - Quirc decoding failures are now actually handled (by skipping them).\n\n### [0.1.2] - 2021-06-16\n\n#### Added\n  - support more image sources, including PIL and bytes objects.\n\n#### Changed\n\n  - package: drop numpy dependency by trying to be clever\n  - decoders: add image binarization to improve decode rate.\n\n### [0.1.1] - 2021-06-06\n\n#### Added\n\n  - decoder.qrdec: expose qr code mask type\n  - decoder.qrdec: compute geometric center of qr code\n  - decoder.quirc: compute geometric center of qr code\n\n### [0.1.0] - 2021-06-04\n\n#### Added\n\n  - Basic QR code decoding functionality\n",
    'author': 'torque',
    'author_email': 'torque@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/torque/deqr',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
