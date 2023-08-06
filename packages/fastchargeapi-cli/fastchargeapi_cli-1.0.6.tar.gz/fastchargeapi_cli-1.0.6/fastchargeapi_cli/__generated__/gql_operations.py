from enum import Enum
from typing import Any, List, Literal, Optional

from gql import Client
from pydantic import BaseModel, Field

from fastchargeapi_cli.graphql_client import gql_execute


class AppFullTextSearchOrderBy(str, Enum):
    exact_match = "exact_match"
    github_popularity = "github_popularity"


class GatewayDecisionResponseReason(str, Enum):
    insufficient_balance = "insufficient_balance"
    owner_insufficient_balance = "owner_insufficient_balance"
    not_subscribed = "not_subscribed"
    too_many_requests = "too_many_requests"
    unknown = "unknown"
    failed_to_create_resource = "failed_to_create_resource"


class UserIndex(str, Enum):
    indexByEmail__onlyPK = "indexByEmail__onlyPK"


class SortDirection(str, Enum):
    ascending = "ascending"
    descending = "descending"


class AppIndex(str, Enum):
    indexByOwner__onlyPK = "indexByOwner__onlyPK"


class AppVisibility(str, Enum):
    public = "public"
    private = "private"


class HTTPMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"


class StripePaymentAcceptStatus(str, Enum):
    pending = "pending"
    settled = "settled"


class GatewayMode(str, Enum):
    proxy = "proxy"
    redirect = "redirect"


class StripeTransferStatus(str, Enum):
    pending = "pending"
    transferred = "transferred"
    failed = "failed"


class StripeTransferIndex(str, Enum):
    indexByStatus_transferAt__onlyPK = "indexByStatus_transferAt__onlyPK"


class AccountActivityType(str, Enum):
    credit = "credit"
    debit = "debit"


class AccountActivityReason(str, Enum):
    payout = "payout"
    payout_fee = "payout_fee"
    topup = "topup"
    api_per_request_charge = "api_per_request_charge"
    api_min_monthly_charge = "api_min_monthly_charge"
    api_min_monthly_charge_upgrade = "api_min_monthly_charge_upgrade"
    fastchargeapi_per_request_service_fee = "fastchargeapi_per_request_service_fee"


class AccountActivityStatus(str, Enum):
    pending = "pending"
    settled = "settled"


class AccountActivityIndex(str, Enum):
    indexByStatus_settleAt__onlyPK = "indexByStatus_settleAt__onlyPK"


class SiteMetaDataKey(str, Enum):
    pricingPerRequestCharge = "pricingPerRequestCharge"
    pricingStripePercentageFee = "pricingStripePercentageFee"
    pricingStripeFlatFee = "pricingStripeFlatFee"


class DateRangeInput(BaseModel):
    start: Optional[int]
    end: Optional[int]


class GetCurrentSubscriptionSubscriptionPricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str


class GetCurrentSubscriptionSubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    pk: str
    pricing: GetCurrentSubscriptionSubscriptionPricing


class GetCurrentSubscription(BaseModel):
    subscription: GetCurrentSubscriptionSubscription

    class Arguments(BaseModel):
        user: Optional[str] = None
        app_name: Optional[str] = None

    class Meta:
        document = "query GetCurrentSubscription($user: ID, $app_name: String) {\n  subscription(subscriber: $user, app: $app_name) {\n    pk\n    pricing {\n      name\n    }\n  }\n}"


class ListAppPricingPksAppPricingplans(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    pk: str
    name: str


class ListAppPricingPksApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    pricingPlans: List[ListAppPricingPksAppPricingplans]


class ListAppPricingPks(BaseModel):
    app: ListAppPricingPksApp

    class Arguments(BaseModel):
        app_name: Optional[str] = None

    class Meta:
        document = "query ListAppPricingPks($app_name: String) {\n  app(name: $app_name) {\n    pricingPlans {\n      pk\n      name\n    }\n  }\n}"


class ListAllSubscriptionsForUserUserSubscriptionsApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str


class ListAllSubscriptionsForUserUserSubscriptionsPricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str
    minMonthlyCharge: str
    chargePerRequest: str


class ListAllSubscriptionsForUserUserSubscriptions(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    app: ListAllSubscriptionsForUserUserSubscriptionsApp
    pricing: ListAllSubscriptionsForUserUserSubscriptionsPricing


class ListAllSubscriptionsForUserUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    subscriptions: List[ListAllSubscriptionsForUserUserSubscriptions]


class ListAllSubscriptionsForUser(BaseModel):
    user: ListAllSubscriptionsForUserUser

    class Arguments(BaseModel):
        user: str

    class Meta:
        document = "query ListAllSubscriptionsForUser($user: ID!) {\n  user(pk: $user) {\n    subscriptions {\n      app {\n        name\n      }\n      pricing {\n        name\n        minMonthlyCharge\n        chargePerRequest\n      }\n    }\n  }\n}"


class SubscribeToAppCreatesubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    pk: str
    createdAt: int


class SubscribeToApp(BaseModel):
    createSubscription: SubscribeToAppCreatesubscription

    class Arguments(BaseModel):
        subscriber: str
        pricing: str

    class Meta:
        document = "mutation SubscribeToApp($subscriber: ID!, $pricing: ID!) {\n  createSubscription(subscriber: $subscriber, pricing: $pricing) {\n    pk\n    createdAt\n  }\n}"


class ChangeSubscriptionSubscriptionUpdatesubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    updatedAt: int


class ChangeSubscriptionSubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    updateSubscription: Optional[ChangeSubscriptionSubscriptionUpdatesubscription]


class ChangeSubscription(BaseModel):
    subscription: ChangeSubscriptionSubscription

    class Arguments(BaseModel):
        subPK: str
        newPricing: str

    class Meta:
        document = "query ChangeSubscription($subPK: ID!, $newPricing: ID!) {\n  subscription(pk: $subPK) {\n    updateSubscription(pricing: $newPricing) {\n      updatedAt\n    }\n  }\n}"


class UnsubscribeFromAppSubscriptionDeletesubscriptionPricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str


class UnsubscribeFromAppSubscriptionDeletesubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    pricing: UnsubscribeFromAppSubscriptionDeletesubscriptionPricing


class UnsubscribeFromAppSubscription(BaseModel):
    typename: Optional[Literal["Subscribe"]] = Field(alias="__typename")
    deleteSubscription: Optional[UnsubscribeFromAppSubscriptionDeletesubscription]


class UnsubscribeFromApp(BaseModel):
    subscription: UnsubscribeFromAppSubscription

    class Arguments(BaseModel):
        subscriber: str
        app: str

    class Meta:
        document = "query UnsubscribeFromApp($subscriber: ID!, $app: String!) {\n  subscription(subscriber: $subscriber, app: $app) {\n    deleteSubscription {\n      pricing {\n        name\n      }\n    }\n  }\n}"


class GetUserByEmailUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    pk: str


class GetUserByEmail(BaseModel):
    user: GetUserByEmailUser

    class Arguments(BaseModel):
        email: str

    class Meta:
        document = "query GetUserByEmail($email: Email!) {\n  user(email: $email) {\n    pk\n  }\n}"


class CreateEndpointCreateendpoint(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    path: str
    description: Optional[str]
    destination: Optional[str]


class CreateEndpoint(BaseModel):
    createEndpoint: CreateEndpointCreateendpoint

    class Arguments(BaseModel):
        app: str
        path: str
        method: HTTPMethod
        destination: str
        description: Optional[str] = None

    class Meta:
        document = "mutation CreateEndpoint($app: ID!, $path: String!, $method: HTTPMethod!, $destination: String!, $description: String) {\n  createEndpoint(\n    app: $app\n    path: $path\n    method: $method\n    destination: $destination\n    description: $description\n  ) {\n    path\n    description\n    destination\n  }\n}"


class GetSecretSecretDeletesecret(BaseModel):
    typename: Optional[Literal["Secret"]] = Field(alias="__typename")
    key: str


class GetSecretSecret(BaseModel):
    typename: Optional[Literal["Secret"]] = Field(alias="__typename")
    value: str
    deleteSecret: Optional[GetSecretSecretDeletesecret]


class GetSecret(BaseModel):
    secret: GetSecretSecret

    class Arguments(BaseModel):
        key: str

    class Meta:
        document = "query GetSecret($key: String!) {\n  secret(key: $key) {\n    value\n    deleteSecret {\n      key\n    }\n  }\n}"


class CreateUserAppTokenUserCreateapptoken(BaseModel):
    typename: Optional[Literal["UserAppToken"]] = Field(alias="__typename")
    token: Optional[str]


class CreateUserAppTokenUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    createAppToken: CreateUserAppTokenUserCreateapptoken


class CreateUserAppToken(BaseModel):
    user: CreateUserAppTokenUser

    class Arguments(BaseModel):
        user: str
        app: str

    class Meta:
        document = "query CreateUserAppToken($user: ID!, $app: ID!) {\n  user(pk: $user) {\n    createAppToken(app: $app) {\n      token\n    }\n  }\n}"


class DeleteUserAppTpkenUserApptokenDeleteuserapptoken(BaseModel):
    typename: Optional[Literal["UserAppToken"]] = Field(alias="__typename")
    token: Optional[str]


class DeleteUserAppTpkenUserApptoken(BaseModel):
    typename: Optional[Literal["UserAppToken"]] = Field(alias="__typename")
    deleteUserAppToken: DeleteUserAppTpkenUserApptokenDeleteuserapptoken


class DeleteUserAppTpkenUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    appToken: DeleteUserAppTpkenUserApptoken


class DeleteUserAppTpken(BaseModel):
    user: DeleteUserAppTpkenUser

    class Arguments(BaseModel):
        user: str
        app: str

    class Meta:
        document = "query DeleteUserAppTpken($user: ID!, $app: ID!) {\n  user(pk: $user) {\n    appToken(app: $app) {\n      deleteUserAppToken {\n        token\n      }\n    }\n  }\n}"


class GetUserAccountBalanceForWithdrawlUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    balance: str
    stripeConnectAccountId: Optional[str]


class GetUserAccountBalanceForWithdrawl(BaseModel):
    user: GetUserAccountBalanceForWithdrawlUser

    class Arguments(BaseModel):
        user: str

    class Meta:
        document = "query GetUserAccountBalanceForWithdrawl($user: ID!) {\n  user(pk: $user) {\n    balance\n    stripeConnectAccountId\n  }\n}"


class UpdateEndpointEndpointUpdateendpoint(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    pk: str
    path: str
    description: Optional[str]
    destination: Optional[str]


class UpdateEndpointEndpoint(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    path: str
    updateEndpoint: UpdateEndpointEndpointUpdateendpoint


class UpdateEndpoint(BaseModel):
    endpoint: UpdateEndpointEndpoint

    class Arguments(BaseModel):
        endpoint: str
        method: Optional[HTTPMethod] = None
        path: Optional[str] = None
        destination: Optional[str] = None
        description: Optional[str] = None

    class Meta:
        document = "query UpdateEndpoint($endpoint: ID!, $method: HTTPMethod, $path: String, $destination: String, $description: String) {\n  endpoint(pk: $endpoint) {\n    path\n    updateEndpoint(\n      method: $method\n      path: $path\n      destination: $destination\n      description: $description\n    ) {\n      pk\n      path\n      description\n      destination\n    }\n  }\n}"


class DeleteEnpointEndpointDeleteendpoint(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    path: str


class DeleteEnpointEndpoint(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    path: str
    deleteEndpoint: DeleteEnpointEndpointDeleteendpoint


class DeleteEnpoint(BaseModel):
    endpoint: DeleteEnpointEndpoint

    class Arguments(BaseModel):
        pk: str

    class Meta:
        document = "query DeleteEnpoint($pk: ID!) {\n  endpoint(pk: $pk) {\n    path\n    deleteEndpoint {\n      path\n    }\n  }\n}"


class CreateAppCreateapp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str


class CreateApp(BaseModel):
    createApp: CreateAppCreateapp

    class Arguments(BaseModel):
        name: str
        owner: str

    class Meta:
        document = "mutation CreateApp($name: String!, $owner: ID!) {\n  createApp(name: $name, owner: $owner) {\n    name\n  }\n}"


class ListAppsOwnedByUserUserAppsOwner(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    author: str


class ListAppsOwnedByUserUserApps(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str
    gatewayMode: GatewayMode
    description: Optional[str]
    owner: ListAppsOwnedByUserUserAppsOwner


class ListAppsOwnedByUserUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    apps: List[ListAppsOwnedByUserUserApps]


class ListAppsOwnedByUser(BaseModel):
    user: ListAppsOwnedByUserUser

    class Arguments(BaseModel):
        user: str

    class Meta:
        document = "query ListAppsOwnedByUser($user: ID!) {\n  user(pk: $user) {\n    apps {\n      name\n      gatewayMode\n      description\n      owner {\n        author\n      }\n    }\n  }\n}"


class GetAppDetailAppOwner(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    author: str


class GetAppDetailApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str
    description: Optional[str]
    gatewayMode: GatewayMode
    owner: GetAppDetailAppOwner


class GetAppDetail(BaseModel):
    app: GetAppDetailApp

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "query GetAppDetail($name: String!) {\n  app(name: $name) {\n    name\n    description\n    gatewayMode\n    owner {\n      author\n    }\n  }\n}"


class DeleteAppAppDeleteapp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str


class DeleteAppApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    deleteApp: DeleteAppAppDeleteapp


class DeleteApp(BaseModel):
    app: DeleteAppApp

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "query DeleteApp($name: String!) {\n  app(name: $name) {\n    deleteApp {\n      name\n    }\n  }\n}"


class UpdateAppAppUpdateapp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    updatedAt: int


class UpdateAppApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    updateApp: UpdateAppAppUpdateapp


class UpdateApp(BaseModel):
    app: UpdateAppApp

    class Arguments(BaseModel):
        app_name: str
        title: Optional[str] = None
        description: Optional[str] = None
        repository: Optional[str] = None
        homepage: Optional[str] = None
        readme: Optional[str] = None
        visibility: Optional[AppVisibility] = None

    class Meta:
        document = "query UpdateApp($app_name: String!, $title: String, $description: String, $repository: URL, $homepage: URL, $readme: URL, $visibility: AppVisibility) {\n  app(name: $app_name) {\n    updateApp(\n      title: $title\n      description: $description\n      repository: $repository\n      homepage: $homepage\n      readme: $readme\n      visibility: $visibility\n    ) {\n      updatedAt\n    }\n  }\n}"


class ListAppPricingDetailsAppPricingplans(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    pk: str
    name: str
    callToAction: str
    minMonthlyCharge: str
    chargePerRequest: str
    freeQuota: int


class ListAppPricingDetailsApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str
    description: Optional[str]
    pricingPlans: List[ListAppPricingDetailsAppPricingplans]


class ListAppPricingDetails(BaseModel):
    app: ListAppPricingDetailsApp

    class Arguments(BaseModel):
        app_name: str

    class Meta:
        document = "query ListAppPricingDetails($app_name: String!) {\n  app(name: $app_name) {\n    name\n    description\n    pricingPlans {\n      pk\n      name\n      callToAction\n      minMonthlyCharge\n      chargePerRequest\n      freeQuota\n    }\n  }\n}"


class CreateAppPricingPlanCreatepricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str


class CreateAppPricingPlan(BaseModel):
    createPricing: CreateAppPricingPlanCreatepricing

    class Arguments(BaseModel):
        app: str
        name: str
        minMonthlyCharge: str
        chargePerRequest: str
        freeQuota: int
        callToAction: Optional[str] = None
        visible: Optional[bool] = None

    class Meta:
        document = "mutation CreateAppPricingPlan($app: ID!, $name: String!, $minMonthlyCharge: NonNegativeDecimal!, $chargePerRequest: NonNegativeDecimal!, $freeQuota: Int!, $callToAction: String, $visible: Boolean) {\n  createPricing(\n    app: $app\n    name: $name\n    callToAction: $callToAction\n    minMonthlyCharge: $minMonthlyCharge\n    chargePerRequest: $chargePerRequest\n    freeQuota: $freeQuota\n    visible: $visible\n  ) {\n    name\n  }\n}"


class UpdateAppPricingPlanPricingUpdatepricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str


class UpdateAppPricingPlanPricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    updatePricing: UpdateAppPricingPlanPricingUpdatepricing


class UpdateAppPricingPlan(BaseModel):
    pricing: UpdateAppPricingPlanPricing

    class Arguments(BaseModel):
        pk: str
        name: Optional[str] = None
        minMonthlyCharge: Optional[str] = None
        chargePerRequest: Optional[str] = None
        freeQuota: Optional[int] = None
        callToAction: Optional[str] = None
        visible: Optional[bool] = None

    class Meta:
        document = "query UpdateAppPricingPlan($pk: ID!, $name: String, $minMonthlyCharge: String, $chargePerRequest: String, $freeQuota: Int, $callToAction: String, $visible: Boolean) {\n  pricing(pk: $pk) {\n    updatePricing(\n      name: $name\n      callToAction: $callToAction\n      minMonthlyCharge: $minMonthlyCharge\n      chargePerRequest: $chargePerRequest\n      freeQuota: $freeQuota\n      visible: $visible\n    ) {\n      name\n    }\n  }\n}"


class GetPricingDetailPricing(BaseModel):
    typename: Optional[Literal["Pricing"]] = Field(alias="__typename")
    name: str
    callToAction: str
    minMonthlyCharge: str
    chargePerRequest: str
    freeQuota: int
    visible: bool


class GetPricingDetail(BaseModel):
    pricing: GetPricingDetailPricing

    class Arguments(BaseModel):
        pk: str

    class Meta:
        document = "query GetPricingDetail($pk: ID!) {\n  pricing(pk: $pk) {\n    name\n    callToAction\n    minMonthlyCharge\n    chargePerRequest\n    freeQuota\n    visible\n  }\n}"


class GetAppEndpointsAppEndpoints(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    pk: str
    path: str
    method: HTTPMethod
    description: Optional[str]


class GetAppEndpointsApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str
    endpoints: List[GetAppEndpointsAppEndpoints]


class GetAppEndpoints(BaseModel):
    app: GetAppEndpointsApp

    class Arguments(BaseModel):
        appName: str

    class Meta:
        document = "query GetAppEndpoints($appName: String!) {\n  app(name: $appName) {\n    name\n    endpoints {\n      pk\n      path\n      method\n      description\n    }\n  }\n}"


class GetAppEndpointsAsOwnerAppEndpoints(BaseModel):
    typename: Optional[Literal["Endpoint"]] = Field(alias="__typename")
    pk: str
    path: str
    method: HTTPMethod
    description: Optional[str]
    destination: Optional[str]


class GetAppEndpointsAsOwnerApp(BaseModel):
    typename: Optional[Literal["App"]] = Field(alias="__typename")
    name: str
    endpoints: List[GetAppEndpointsAsOwnerAppEndpoints]


class GetAppEndpointsAsOwner(BaseModel):
    app: GetAppEndpointsAsOwnerApp

    class Arguments(BaseModel):
        appName: str

    class Meta:
        document = "query GetAppEndpointsAsOwner($appName: String!) {\n  app(name: $appName) {\n    name\n    endpoints {\n      pk\n      path\n      method\n      description\n      destination\n    }\n  }\n}"


class GetUserAccountBalanceAndLimitUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    balance: str
    balanceLimit: str


class GetUserAccountBalanceAndLimit(BaseModel):
    user: GetUserAccountBalanceAndLimitUser

    class Arguments(BaseModel):
        user: str

    class Meta:
        document = "query GetUserAccountBalanceAndLimit($user: ID!) {\n  user(pk: $user) {\n    balance\n    balanceLimit\n  }\n}"


class UpdateUserInfoUserUpdateuser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    author: str


class UpdateUserInfoUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    updateUser: Optional[UpdateUserInfoUserUpdateuser]


class UpdateUserInfo(BaseModel):
    user: UpdateUserInfoUser

    class Arguments(BaseModel):
        user: str
        author: Optional[str] = None

    class Meta:
        document = "query UpdateUserInfo($user: ID!, $author: String) {\n  user(pk: $user) {\n    updateUser(author: $author) {\n      author\n    }\n  }\n}"


class GetUserAccountInfoUser(BaseModel):
    typename: Optional[Literal["User"]] = Field(alias="__typename")
    balance: str
    author: str
    email: str


class GetUserAccountInfo(BaseModel):
    user: GetUserAccountInfoUser

    class Arguments(BaseModel):
        user: str

    class Meta:
        document = "query GetUserAccountInfo($user: ID!) {\n  user(pk: $user) {\n    balance\n    author\n    email\n  }\n}"


class GetStripePricingDataSitemetadata(BaseModel):
    typename: Optional[Literal["SiteMetaData"]] = Field(alias="__typename")
    key: SiteMetaDataKey
    value: Any


class GetStripePricingData(BaseModel):
    siteMetaData: List[GetStripePricingDataSitemetadata]

    class Arguments(BaseModel):
        pass

    class Meta:
        document = "query GetStripePricingData {\n  siteMetaData(keys: [pricingStripeFlatFee, pricingStripePercentageFee]) {\n    key\n    value\n  }\n}"


def get_current_subscription(
    client: Client, user: Optional[str] = None, app_name: Optional[str] = None
) -> GetCurrentSubscriptionSubscription:
    """GetCurrentSubscription



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (Optional[str], optional): user.
        app_name (Optional[str], optional): app_name.

    Returns:
        GetCurrentSubscriptionSubscription"""
    return gql_execute(
        client, GetCurrentSubscription, {"user": user, "app_name": app_name}
    ).subscription


def list_app_pricing_pks(
    client: Client, app_name: Optional[str] = None
) -> ListAppPricingPksApp:
    """ListAppPricingPks



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        app_name (Optional[str], optional): app_name.

    Returns:
        ListAppPricingPksApp"""
    return gql_execute(client, ListAppPricingPks, {"app_name": app_name}).app


def list_all_subscriptions_for_user(
    client: Client, user: str
) -> ListAllSubscriptionsForUserUser:
    """ListAllSubscriptionsForUser



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user

    Returns:
        ListAllSubscriptionsForUserUser"""
    return gql_execute(client, ListAllSubscriptionsForUser, {"user": user}).user


def subscribe_to_app(
    client: Client, subscriber: str, pricing: str
) -> SubscribeToAppCreatesubscription:
    """SubscribeToApp



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        subscriber (str): subscriber
        pricing (str): pricing

    Returns:
        SubscribeToAppCreatesubscription"""
    return gql_execute(
        client, SubscribeToApp, {"subscriber": subscriber, "pricing": pricing}
    ).createSubscription


def change_subscription(
    client: Client, subPK: str, newPricing: str
) -> ChangeSubscriptionSubscription:
    """ChangeSubscription



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        subPK (str): subPK
        newPricing (str): newPricing

    Returns:
        ChangeSubscriptionSubscription"""
    return gql_execute(
        client, ChangeSubscription, {"subPK": subPK, "newPricing": newPricing}
    ).subscription


def unsubscribe_from_app(
    client: Client, subscriber: str, app: str
) -> UnsubscribeFromAppSubscription:
    """UnsubscribeFromApp



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        subscriber (str): subscriber
        app (str): app

    Returns:
        UnsubscribeFromAppSubscription"""
    return gql_execute(
        client, UnsubscribeFromApp, {"subscriber": subscriber, "app": app}
    ).subscription


def get_user_by_email(client: Client, email: str) -> GetUserByEmailUser:
    """GetUserByEmail



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        email (str): email

    Returns:
        GetUserByEmailUser"""
    return gql_execute(client, GetUserByEmail, {"email": email}).user


def create_endpoint(
    client: Client,
    app: str,
    path: str,
    method: HTTPMethod,
    destination: str,
    description: Optional[str] = None,
) -> CreateEndpointCreateendpoint:
    """CreateEndpoint



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        app (str): app
        path (str): path
        method (HTTPMethod): method
        destination (str): destination
        description (Optional[str], optional): description.

    Returns:
        CreateEndpointCreateendpoint"""
    return gql_execute(
        client,
        CreateEndpoint,
        {
            "app": app,
            "path": path,
            "method": method,
            "destination": destination,
            "description": description,
        },
    ).createEndpoint


def get_secret(client: Client, key: str) -> GetSecretSecret:
    """GetSecret



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        key (str): key

    Returns:
        GetSecretSecret"""
    return gql_execute(client, GetSecret, {"key": key}).secret


def create_user_app_token(
    client: Client, user: str, app: str
) -> CreateUserAppTokenUser:
    """CreateUserAppToken



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user
        app (str): app

    Returns:
        CreateUserAppTokenUser"""
    return gql_execute(client, CreateUserAppToken, {"user": user, "app": app}).user


def delete_user_app_tpken(
    client: Client, user: str, app: str
) -> DeleteUserAppTpkenUser:
    """DeleteUserAppTpken



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user
        app (str): app

    Returns:
        DeleteUserAppTpkenUser"""
    return gql_execute(client, DeleteUserAppTpken, {"user": user, "app": app}).user


def get_user_account_balance_for_withdrawl(
    client: Client, user: str
) -> GetUserAccountBalanceForWithdrawlUser:
    """GetUserAccountBalanceForWithdrawl



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user

    Returns:
        GetUserAccountBalanceForWithdrawlUser"""
    return gql_execute(client, GetUserAccountBalanceForWithdrawl, {"user": user}).user


def update_endpoint(
    client: Client,
    endpoint: str,
    method: Optional[HTTPMethod] = None,
    path: Optional[str] = None,
    destination: Optional[str] = None,
    description: Optional[str] = None,
) -> UpdateEndpointEndpoint:
    """UpdateEndpoint



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        endpoint (str): endpoint
        method (Optional[HTTPMethod], optional): method.
        path (Optional[str], optional): path.
        destination (Optional[str], optional): destination.
        description (Optional[str], optional): description.

    Returns:
        UpdateEndpointEndpoint"""
    return gql_execute(
        client,
        UpdateEndpoint,
        {
            "endpoint": endpoint,
            "method": method,
            "path": path,
            "destination": destination,
            "description": description,
        },
    ).endpoint


def delete_enpoint(client: Client, pk: str) -> DeleteEnpointEndpoint:
    """DeleteEnpoint



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        pk (str): pk

    Returns:
        DeleteEnpointEndpoint"""
    return gql_execute(client, DeleteEnpoint, {"pk": pk}).endpoint


def create_app(client: Client, name: str, owner: str) -> CreateAppCreateapp:
    """CreateApp



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        name (str): name
        owner (str): owner

    Returns:
        CreateAppCreateapp"""
    return gql_execute(client, CreateApp, {"name": name, "owner": owner}).createApp


def list_apps_owned_by_user(client: Client, user: str) -> ListAppsOwnedByUserUser:
    """ListAppsOwnedByUser



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user

    Returns:
        ListAppsOwnedByUserUser"""
    return gql_execute(client, ListAppsOwnedByUser, {"user": user}).user


def get_app_detail(client: Client, name: str) -> GetAppDetailApp:
    """GetAppDetail



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        name (str): name

    Returns:
        GetAppDetailApp"""
    return gql_execute(client, GetAppDetail, {"name": name}).app


def delete_app(client: Client, name: str) -> DeleteAppApp:
    """DeleteApp



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        name (str): name

    Returns:
        DeleteAppApp"""
    return gql_execute(client, DeleteApp, {"name": name}).app


def update_app(
    client: Client,
    app_name: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    repository: Optional[str] = None,
    homepage: Optional[str] = None,
    readme: Optional[str] = None,
    visibility: Optional[AppVisibility] = None,
) -> UpdateAppApp:
    """UpdateApp



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        app_name (str): app_name
        title (Optional[str], optional): title.
        description (Optional[str], optional): description.
        repository (Optional[str], optional): repository.
        homepage (Optional[str], optional): homepage.
        readme (Optional[str], optional): readme.
        visibility (Optional[AppVisibility], optional): visibility.

    Returns:
        UpdateAppApp"""
    return gql_execute(
        client,
        UpdateApp,
        {
            "app_name": app_name,
            "title": title,
            "description": description,
            "repository": repository,
            "homepage": homepage,
            "readme": readme,
            "visibility": visibility,
        },
    ).app


def list_app_pricing_details(client: Client, app_name: str) -> ListAppPricingDetailsApp:
    """ListAppPricingDetails



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        app_name (str): app_name

    Returns:
        ListAppPricingDetailsApp"""
    return gql_execute(client, ListAppPricingDetails, {"app_name": app_name}).app


def create_app_pricing_plan(
    client: Client,
    app: str,
    name: str,
    minMonthlyCharge: str,
    chargePerRequest: str,
    freeQuota: int,
    callToAction: Optional[str] = None,
    visible: Optional[bool] = None,
) -> CreateAppPricingPlanCreatepricing:
    """CreateAppPricingPlan



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        app (str): app
        name (str): name
        minMonthlyCharge (str): minMonthlyCharge
        chargePerRequest (str): chargePerRequest
        freeQuota (int): freeQuota
        callToAction (Optional[str], optional): callToAction.
        visible (Optional[bool], optional): visible.

    Returns:
        CreateAppPricingPlanCreatepricing"""
    return gql_execute(
        client,
        CreateAppPricingPlan,
        {
            "app": app,
            "name": name,
            "minMonthlyCharge": minMonthlyCharge,
            "chargePerRequest": chargePerRequest,
            "freeQuota": freeQuota,
            "callToAction": callToAction,
            "visible": visible,
        },
    ).createPricing


def update_app_pricing_plan(
    client: Client,
    pk: str,
    name: Optional[str] = None,
    minMonthlyCharge: Optional[str] = None,
    chargePerRequest: Optional[str] = None,
    freeQuota: Optional[int] = None,
    callToAction: Optional[str] = None,
    visible: Optional[bool] = None,
) -> UpdateAppPricingPlanPricing:
    """UpdateAppPricingPlan



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        pk (str): pk
        name (Optional[str], optional): name.
        minMonthlyCharge (Optional[str], optional): minMonthlyCharge.
        chargePerRequest (Optional[str], optional): chargePerRequest.
        freeQuota (Optional[int], optional): freeQuota.
        callToAction (Optional[str], optional): callToAction.
        visible (Optional[bool], optional): visible.

    Returns:
        UpdateAppPricingPlanPricing"""
    return gql_execute(
        client,
        UpdateAppPricingPlan,
        {
            "pk": pk,
            "name": name,
            "minMonthlyCharge": minMonthlyCharge,
            "chargePerRequest": chargePerRequest,
            "freeQuota": freeQuota,
            "callToAction": callToAction,
            "visible": visible,
        },
    ).pricing


def get_pricing_detail(client: Client, pk: str) -> GetPricingDetailPricing:
    """GetPricingDetail



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        pk (str): pk

    Returns:
        GetPricingDetailPricing"""
    return gql_execute(client, GetPricingDetail, {"pk": pk}).pricing


def get_app_endpoints(client: Client, appName: str) -> GetAppEndpointsApp:
    """GetAppEndpoints



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        appName (str): appName

    Returns:
        GetAppEndpointsApp"""
    return gql_execute(client, GetAppEndpoints, {"appName": appName}).app


def get_app_endpoints_as_owner(
    client: Client, appName: str
) -> GetAppEndpointsAsOwnerApp:
    """GetAppEndpointsAsOwner



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        appName (str): appName

    Returns:
        GetAppEndpointsAsOwnerApp"""
    return gql_execute(client, GetAppEndpointsAsOwner, {"appName": appName}).app


def get_user_account_balance_and_limit(
    client: Client, user: str
) -> GetUserAccountBalanceAndLimitUser:
    """GetUserAccountBalanceAndLimit



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user

    Returns:
        GetUserAccountBalanceAndLimitUser"""
    return gql_execute(client, GetUserAccountBalanceAndLimit, {"user": user}).user


def update_user_info(
    client: Client, user: str, author: Optional[str] = None
) -> UpdateUserInfoUser:
    """UpdateUserInfo



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user
        author (Optional[str], optional): author.

    Returns:
        UpdateUserInfoUser"""
    return gql_execute(client, UpdateUserInfo, {"user": user, "author": author}).user


def get_user_account_info(client: Client, user: str) -> GetUserAccountInfoUser:
    """GetUserAccountInfo



    Arguments:
        client (gql.Client): The client we want to use to execute the operation
        user (str): user

    Returns:
        GetUserAccountInfoUser"""
    return gql_execute(client, GetUserAccountInfo, {"user": user}).user


def get_stripe_pricing_data(client: Client) -> List[GetStripePricingDataSitemetadata]:
    """GetStripePricingData



    Arguments:
        client (gql.Client): The client we want to use to execute the operation

    Returns:
        List[GetStripePricingDataSitemetadata]"""
    return gql_execute(client, GetStripePricingData, {}).siteMetaData
