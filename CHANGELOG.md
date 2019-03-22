# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

## [0.1.8] - 2019-03-22
### Fixed
- Handle error responses containing `status` instead of `result`.

## [0.1.7] - 2019-03-21
### Added
- `get_servers` method
- `module_create` method

### Fixed
- Processing of array params, lists are now processed properly.

## [0.1.6] - 2019-02-25
### Added
- `get_orders` method
- `cancel_order` method
- `delete_order` method
- `pending_order` method

## [0.1.5] - 2019-02-05
### Added
- `add_transaction` method
- `get_invoice` method
- `get_tickets` method
- `get_transactions` method
- `open_ticket` method
- `send_email` method

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
[0.1.8]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.8
[0.1.7]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.7
[0.1.6]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.6
[0.1.5]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.5
[0.1.4]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.4
[0.1.3]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.3
[0.1.2]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.2
[0.1.1]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.1
[0.1.0]: https://github.com/Smoose-bv/whmcspy/releases/tag/0.1.0
