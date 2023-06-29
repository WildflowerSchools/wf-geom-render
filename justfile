lint:
    pylint geom_render

format:
    black geom_render

build:
    poetry build

publish: build
    poetry publish --skip-existing
