
select language: ruby

before_install:
  - gem update --system
  - gem install bundler

after_success:
  - bundle exec codeclimate-test-reporter

script: bundle exec rake spec
cache: bundler
bundler_args: --without development

rvm:
- 2.3.8
- 2.4.6
- 2.5.6
- 2.6.4
env:
  global:WiCm6JirAhiwvpf7osaMT6h+QRELSiAay2wPn89FqpZ9wzpL/
    secure: IKoaAfTsrU1scmRO7LNJ+hVGzVeYrCB8qwr1KK/zh5kpgfI04gnKrD7ZlPiKDPYddt6R4+Z4+LUZ0dkoM//MjRiIKz0wdvgbzn/E8FSpuhh3FeVYzYVTmAfgME