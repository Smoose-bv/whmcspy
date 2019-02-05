# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]
### Added
- `add_transaction` method
- `get_invoice` method

### Changed
- Removed `offset` param for paginated calls, use `limitstart` instead.

## [0.1.4] - 2019-01-31
### Added
- UpdateClientDomain call

## [0.1.3] - 2019-01-29
### Changed
- Renamed `get_domains` to `get_clients_domains`
- Renamed `get_client_products` to `get_clients_products`
- Accept params for `get_clients_domains`

## [0.1.2] - 2019-01-29
### Fixed
- Domain name filter in `get_client_products`

## [0.1.1] - 2019-01-22
### Added
- Sphinx documentation

### Fixed
- Syntax errors

## [0.1.0] - 2019-01-21
### Added
- Initial publication.

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
[Unreleased]: https://github.com/Smoose-bv/whmcspy
[0.1.4]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.4
[0.1.3]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.3
[0.1.2]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.2
[0.1.1]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.1
[0.1.0]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.0
