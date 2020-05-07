from peering.constants import *
from peering.filters import (
    AutonomousSystemFilterSet,
    BGPGroupFilterSet,
    CommunityFilterSet,
    DirectPeeringSessionFilterSet,
    InternetExchangeFilterSet,
    InternetExchangePeeringSessionFilterSet,
    RouterFilterSet,
    RoutingPolicyFilterSet,
    TemplateFilterSet,
)
from peering.models import (
    AutonomousSystem,
    BGPGroup,
    Community,
    DirectPeeringSession,
    InternetExchange,
    InternetExchangePeeringSession,
    Router,
    RoutingPolicy,
    Template,
)
from utils.testing import StandardTestCases


class AutonomousSystemTestCase(StandardTestCases.Filters):
    model = AutonomousSystem
    filter = AutonomousSystemFilterSet

    @classmethod
    def setUpTestData(cls):
        AutonomousSystem.objects.bulk_create(
            [
                AutonomousSystem(
                    asn=64501,
                    name="Autonomous System 1",
                    irr_as_set="AS-SET-1",
                    ipv6_max_prefixes=1,
                    ipv4_max_prefixes=0,
                ),
                AutonomousSystem(
                    asn=64502,
                    name="Autonomous System 2",
                    irr_as_set="AS-SET-2",
                    ipv6_max_prefixes=0,
                    ipv4_max_prefixes=1,
                ),
                AutonomousSystem(
                    asn=64503,
                    name="Autonomous System 3",
                    irr_as_set="AS-SET-3",
                    ipv6_max_prefixes=0,
                    ipv4_max_prefixes=0,
                ),
            ]
        )

    def test_asn(self):
        params = {"asn": 64501}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {"name": "Autonomous System 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_irr_as_set(self):
        params = {"irr_as_set": "AS-SET-1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_ipv6_max_prefixes(self):
        params = {"ipv6_max_prefixes": 1}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
        params = {"ipv6_max_prefixes": 0}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)

    def test_ipv4_max_prefixes(self):
        params = {"ipv4_max_prefixes": 1}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
        params = {"ipv4_max_prefixes": 0}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)


class BGPGroupTestCase(StandardTestCases.Filters):
    model = BGPGroup
    filter = BGPGroupFilterSet

    @classmethod
    def setUpTestData(cls):
        BGPGroup.objects.bulk_create(
            [
                BGPGroup(name="BGP Group 1", slug="bgp-group-1"),
                BGPGroup(name="BGP Group 2", slug="bgp-group-2"),
                BGPGroup(name="BGP Group 3", slug="bgp-group-3"),
            ]
        )

    def test_name(self):
        params = {"name": "BGP Group 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)


class CommunityTestCase(StandardTestCases.Filters):
    model = Community
    filter = CommunityFilterSet

    @classmethod
    def setUpTestData(cls):
        Community.objects.bulk_create(
            [
                Community(
                    name="Community 1", description="community1", value="64500:1", type=COMMUNITY_TYPE_EGRESS
                ),
                Community(name="Community 2",description="community2", value="64500:2"),
                Community(name="Community 3",description="community3", value="64500:3"),
            ]
        )

    def test_name(self):
        params = {"name": "Community 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_type(self):
        params = {"type": COMMUNITY_TYPE_INGRESS}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)

    def test_value(self):
        params = {"value": "64500:1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_description(self):
        params = {"description": "community2"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)


class DirectPeeringSessionTestCase(StandardTestCases.Filters):
    model = DirectPeeringSession
    filter = DirectPeeringSessionFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.a_s = AutonomousSystem.objects.create(asn=64501, name="Autonomous System 1")
        cls.router = Router.objects.create(
            name="Router 1", hostname="router1.example.net"
        )
        DirectPeeringSession.objects.bulk_create(
            [
                DirectPeeringSession(
                    local_asn=64500,
                    autonomous_system=cls.a_s,
                    ip_address="192.0.2.1",
                    relationship=BGP_RELATIONSHIP_TRANSIT_PROVIDER,
                    router=cls.router,
                ),
                DirectPeeringSession(
                    local_asn=64500,
                    autonomous_system=cls.a_s,
                    ip_address="192.0.2.2",
                    relationship=BGP_RELATIONSHIP_PRIVATE_PEERING,
                    multihop_ttl=2,
                ),
                DirectPeeringSession(
                    local_asn=64500,
                    autonomous_system=cls.a_s,
                    ip_address="192.0.2.3",
                    relationship=BGP_RELATIONSHIP_CUSTOMER,
                    enabled=False,
                ),
            ]
        )

    def test_address_family(self):
        params = {"address_family": 4}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)
        params = {"address_family": 6}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 0)

    def test_relationship(self):
        params = {"relationship": [BGP_RELATIONSHIP_TRANSIT_PROVIDER]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_router(self):
        params = {"router": [self.router]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_local_asn(self):
        params = {"local_asn": 64500}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)
        params = {"local_asn": 64501}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 0)

    def test_multihop_ttl(self):
        params = {"multihop_ttl": 1}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"multihop_ttl": 2}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_enabled(self):
        params = {"enabled": True}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"enabled": False}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)


class InternetExchangeTestCase(StandardTestCases.Filters):
    model = InternetExchange
    filter = InternetExchangeFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.router = Router.objects.create(
            name="Router 1", hostname="router1.example.net"
        )
        InternetExchange.objects.bulk_create(
            [
                InternetExchange(name="Internet Exchange 1", slug="ix-1"),
                InternetExchange(name="Internet Exchange 2", slug="ix-2"),
                InternetExchange(
                    name="Internet Exchange 3", slug="ix-3", router=cls.router
                ),
            ]
        )

    def test_router(self):
        params = {"router": [self.router]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {"name": "Internet Exchange 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_slug(self):
        params = {"slug": "ix-1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)


class InternetExchangePeeringSessionTestCase(StandardTestCases.Filters):
    model = InternetExchangePeeringSession
    filter = InternetExchangePeeringSessionFilterSet

    @classmethod
    def setUpTestData(cls):
        cls.a_s = AutonomousSystem.objects.create(asn=64501, name="Autonomous System 1")
        cls.ix = InternetExchange.objects.create(
            name="Internet Exchange 1", slug="ix-1"
        )
        InternetExchangePeeringSession.objects.bulk_create(
            [
                InternetExchangePeeringSession(
                    autonomous_system=cls.a_s,
                    internet_exchange=cls.ix,
                    ip_address="192.0.2.1",
                    multihop_ttl=2,
                ),
                InternetExchangePeeringSession(
                    autonomous_system=cls.a_s,
                    internet_exchange=cls.ix,
                    ip_address="192.0.2.2",
                    enabled=False,
                ),
                InternetExchangePeeringSession(
                    autonomous_system=cls.a_s,
                    internet_exchange=cls.ix,
                    ip_address="192.0.2.3",
                    is_route_server=True,
                ),
            ]
        )

    def test_address_family(self):
        params = {"address_family": 4}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)
        params = {"address_family": 6}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 0)

    def test_multihop_ttl(self):
        params = {"multihop_ttl": 1}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"multihop_ttl": 2}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_enabled(self):
        params = {"enabled": True}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"enabled": False}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_is_route_server(self):
        params = {"is_route_server": False}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"is_route_server": True}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_autonomous_system__asn(self):
        params = {"autonomous_system__asn": 64501}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)
        params = {"autonomous_system__asn": 64500}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 0)

    def test_autonomous_system__id(self):
        params = {"autonomous_system__id": self.a_s.id}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)

    def test_autonomous_system__name(self):
        params = {"autonomous_system__name": self.a_s.name}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)

    def test_internet_exchange__id(self):
        params = {"internet_exchange__id": self.ix.id}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)

    def test_internet_exchange__name(self):
        params = {"internet_exchange__name": self.ix.name}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)


class RouterTestCase(StandardTestCases.Filters):
    model = Router
    filter = RouterFilterSet

    @classmethod
    def setUpTestData(cls):
        Router.objects.bulk_create(
            [
                Router(
                    name="Router 1",
                    hostname="router1.example.net",
                    platform=PLATFORM_JUNOS,
                ),
                Router(
                    name="Router 2",
                    hostname="router2.example.net",
                    platform=PLATFORM_IOSXR,
                ),
                Router(name="Router 3", hostname="router3.example.net"),
            ]
        )

    def test_platform(self):
        params = {"platform": [PLATFORM_JUNOS]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
        params = {"platform": [PLATFORM_JUNOS, PLATFORM_IOSXR]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)

    def test_name(self):
        params = {"name": "Router 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_hostname(self):
        params = {"hostname": "router1.example.net"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)


class RoutingPolicyTestCase(StandardTestCases.Filters):
    model = RoutingPolicy
    filter = RoutingPolicyFilterSet

    @classmethod
    def setUpTestData(cls):
        RoutingPolicy.objects.bulk_create(
            [
                RoutingPolicy(
                    name="Routing Policy 1",
                    slug="routing-policy-1",
                    type=ROUTING_POLICY_TYPE_EXPORT,
                    weight=0,
                ),
                RoutingPolicy(
                    name="Routing Policy 2",
                    slug="routing-policy-2",
                    type=ROUTING_POLICY_TYPE_IMPORT,
                    weight=0,
                    address_family=6,
                ),
                RoutingPolicy(
                    name="Routing Policy 3",
                    slug="routing-policy-3",
                    type=ROUTING_POLICY_TYPE_IMPORT_EXPORT,
                    weight=10,
                ),
            ]
        )

    def test_type(self):
        params = {"type": [ROUTING_POLICY_TYPE_IMPORT]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"type": [ROUTING_POLICY_TYPE_EXPORT]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"type": [ROUTING_POLICY_TYPE_IMPORT_EXPORT]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_name(self):
        params = {"name": "Routing Policy 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_slug(self):
        params = {"slug": "routing-policy-1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_weight(self):
        params = {"weight": 0}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"weight": 10}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)

    def test_address_family(self):
        params = {"address_family": 6}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
        params = {"address_family": 4}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 0)


class TemplateTestCase(StandardTestCases.Filters):
    model = Template
    filter = TemplateFilterSet

    @classmethod
    def setUpTestData(cls):
        Template.objects.bulk_create(
            [
                Template(
                    name="Template 1",
                    type=TEMPLATE_TYPE_CONFIGURATION,
                    template="Template 1",
                ),
                Template(
                    name="Template 2",
                    type=TEMPLATE_TYPE_CONFIGURATION,
                    template="Template 2",
                ),
                Template(
                    name="Template 3", type=TEMPLATE_TYPE_EMAIL, template="Template 3"
                ),
            ]
        )

    def test_type(self):
        params = {"type": [TEMPLATE_TYPE_CONFIGURATION]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 2)
        params = {"type": [TEMPLATE_TYPE_EMAIL]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
        params = {"type": [TEMPLATE_TYPE_CONFIGURATION, TEMPLATE_TYPE_EMAIL]}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 3)

    def test_name(self):
        params = {"name": "Template 1"}
        self.assertEqual(self.filter(params, self.queryset).qs.count(), 1)
