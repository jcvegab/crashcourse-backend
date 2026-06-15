"""
env_adapter.py

Detects the hosting platform and normalizes its specific variables
into a common interface. settings.py simply uses this interface.

To add a new platform (Railway, Fly.io, etc.):
  1. Create a subclass of PlatformAdapter
  2. Define _is_active() and _normalize()
  3. Add it to PLATFORM_ADAPTERS
"""

import os
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Standardized interface that settings.py consumes
# ---------------------------------------------------------------------------

@dataclass
class EnvironmentConfig:
    is_production: bool = False
    external_hostname: str = ""
    extra_allowed_hosts: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Adapters by platform
# ---------------------------------------------------------------------------

class PlatformAdapter:
    """Base class. Every platform inherits from here."""

    def _is_active(self) -> bool:
        """Returns True if we are running on this platform."""
        raise NotImplementedError

    def _normalize(self) -> EnvironmentConfig:
        """Translates the platform-specific variables to EnvironmentConfig."""
        raise NotImplementedError

    def detect(self) -> EnvironmentConfig | None:
        """Returns the normalized config if this platform is active, or None."""
        if self._is_active():
            return self._normalize()
        return None


class RenderAdapter(PlatformAdapter):
    """
    Render.com automatically injects:
      - RENDER=true
      - RENDER_EXTERNAL_HOSTNAME=<tu-servicio>.onrender.com
    """

    def _is_active(self) -> bool:
        return os.environ.get("RENDER", "").lower() == "true"

    def _normalize(self) -> EnvironmentConfig:
        hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
        return EnvironmentConfig(
            is_production=True,
            external_hostname=hostname,
            extra_allowed_hosts=[hostname] if hostname else [],
        )


# ---------------------------------------------------------------------------
# Add new platforms here when necessary
#
# class AWSAdapter(PlatformAdapter):
#     """
#     AWS does not automatically inject environment variables like Render.
#     Discovery is based on AWS_EXECUTION_ENV (present in Lambda and ECS)
#     or on a custom variable that you set yourself in EC2/Elastic Beanstalk.
#     The hostname is taken from AWS_HOSTNAME (a variable you must define)
#     pointing to your domain or the load balancer's DNS.
#     """
#     def _is_active(self):
#         return (
#             bool(os.environ.get("AWS_EXECUTION_ENV"))       # Lambda / ECS
#             or os.environ.get("AWS_ENV") == "production"    # EC2 / EB (manual)
#         )
#
#     def _normalize(self):
#         hostname = os.environ.get("AWS_HOSTNAME", "")
#         return EnvironmentConfig(
#             is_production=True,
#             external_hostname=hostname,
#             extra_allowed_hosts=[hostname] if hostname else [],
#         )
#
# ---------------------------------------------------------------------------

PLATFORM_ADAPTERS: list[PlatformAdapter] = [
    RenderAdapter(),
    # AWSAdapter(),
]


# ---------------------------------------------------------------------------
# Main function — the only thing settings.py needs to import
# ---------------------------------------------------------------------------

def get_environment_config() -> EnvironmentConfig:
    """
    Iterates through the adapters in order and returns the configuration of the first one it detects
    as an active platform. If none apply, it returns the development configuration.
    """
    for adapter in PLATFORM_ADAPTERS:
        config = adapter.detect()
        if config is not None:
            return config

    return EnvironmentConfig(is_production=False)