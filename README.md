# RFC: HoloNet Protocol (HLN/1.0)

**Author:** Sam Toxopeus
**Date:** June 3, 2024

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Terminology](#2-terminology)
3. [HoloNet Protocol Specification](#3-holonet-protocol-specification)
    1. [Request Format](#31-request-format)
    2. [Response Format](#32-response-format)
    3. [Methods](#33-methods)
4. [Example](#4-example)
5. [Security Considerations](#5-security-considerations)
6[References](#6-references)

---

## 1. Introduction

The HoloNet (HLN) protocol is a text-based protocol designed for simple client-server communication. It is similar to HTTP but simplified for ease of implementation and use.

---

## 2. Terminology

- **Client**: The entity that initiates a request to the server.
- **Server**: The entity that processes the request and returns a response.
- **HoloHeader**: The first line of the request message, containing the method, resource, and protocol version.
- **HoloHeader**: The first line of the response message, containing the protocol version, status code, and status message.
- **Client/Server Key**: GPG public key of the client or server, encoded as bas64 string.
- **Headers**: Key-value pairs that provide additional information about the request or response.
- **Body**: Optional data sent after the headers in a request or response.

---

## 3. HoloNet Protocol Specification

### 3.1 Request Format

A HoloNet request consists of a HoloHeader, client key, optional headers, and an optional body. The format is as follows:

```
<protocol/version> <method> <resource>
<empty line>
<client key>
<empty line>
<Header-Key>: <Header-Value>
...
<empty line>
<optional body>
```

- **HoloHeader**: 
  - `<protocol/version>`The version of the HoloNet protocol, usually `HLN/1.0`
  - `<method>`: The action to be performed (e.g., READ, WRITE).
  - `<resource>`: The target resource (e.g., / or /resource-name).

- **Client key**
  - This should be the public key of the client making the request, encoded in base64 on a single line. The server uses this for encrypting the response.

- **Headers**: 
  - Each header is a key-value pair separated by a colon and space.

- **Body**: 
  - The body is optional.

### 3.2 Response Format

A HoloNet request consists of a HoloHeader, server key, optional headers, and an optional body. The format is as follows:

```
<protocol/version> <status_code> <status_message>
<empty line>
<server key>
<empty line>
<Header-Key>: <Header-Value>
...
<empty line>
<optional body>
```


- **Status Line**: 
  - `<protocol/version>`The version of the HoloNet protocol, usually `HLN/1.0`
  - `<status_code>`: A three-digit number indicating the result of the request (e.g., 200, 404).
  - `<status_message>`: A single word description of the status code (e.g., OK, NOT_FOUND).

- **Server key**
  - This should be the public key of the server sending the response, encoded in base64 on a single line. The client uses this for encrypting subsequent requests.

- **Headers**: 
  - Each header is a key-value pair separated by a colon and space.

- **Body**: 
  - The body is optional and follows an empty line after the headers.

### 3.3 Methods

- **READ**: Requests the specified resource.
- **WRITE**: Submits data to the specified resource.

---

## 4. Example

### Request
```
HLN/1.0 WRITE /update-user/12

LS0tLS1CRUdJTiBQR1AgUFVCTElDIEtFWSBCTE9DSy0tLS0tCgptUUVOQkdaZUIvTUJDQURjS3RoeFZHWTZ2YXNOZ09Dby93c0RHY2tsb2hPZmJFUmorUlpvOXgzUDZaZ3JiMVhGCkVrcUpacHExbWgrRTlQOXVzeGQyYXVYankrbTJVL3RUN25GR0hZOHF0WHEvemxsVjZrS3pWKzNkdGNJNlpSUGUKVkJUZjRtTThhSGQ5S2hVTWVKbXNDL2YxWGJCTzF0djlWS2dkc3dLY0pQdEdsVlFOeWRRaktSNWlieEZuVEdGNAplaGZwajljWVpmc1RzM2oxL2Q0ZU5FUW9OMWRaM2o2bVAwZlJJM2o5VmVGdXNCKzdPSW0vMVFCS0FqMTIxY1VtCjhWb2J1NVNkNm5YaG85NTQ2WFFiRDd1NFl1U25McUpJT2JXUXQzS0ptamJKL212TEFJTGF6VkFWeEEyd1gyMC8KdUlPTDJyNVRUSWFjWVZ3TlhuUkJvbVVyVDVFdE45ZlpxZSszQUJFQkFBRzBEVWh2Ykc5dVpYUkRiR2xsYm5TSgpBVkVFRXdFSUFEc1dJUVNRdmQyN2hqd3VSRm16KzY2N01aOVdCeFd2RUFVQ1psNEg4d0liQXdVTENRZ0hBZ0lpCkFnWVZDZ2tJQ3dJRUZnSURBUUllQndJWGdBQUtDUkM3TVo5V0J4V3ZFTjVKQi85ZVl2bG1OTjExcUhwaHBuM1EKVVpqNkxuZXU5OEtqWTBhY0hkOVZwQk5FOU81T1BXa3VJTlc0TndtaWRCOFRaYkcvNFNhYUIzMG5zYjJudnNPQwpSMTVzNytZRDlrODY3Z0N3d1lEaVczejNrMlVqT2hSWWVVTGI3c3Zqd0oydlVObllKMmtSTFB2czNuOWFxdTErCjhlTGJtd01MMXdRaC81UHlaSlIyZTNSZWtJM0hacldmTzllcmlVTk9zb2tuazNBV2NnMHo5dFY2eTZLVUdmZUgKS0RqamxackkxR2t4ZWdmR0krUGRjNnlBS0lwaXZNM21Ja3RSNGN1UzRtNWFZT2dCR0J5bW9PQ1Zadk81Z3piZQpMenlndHlWZDhNWXFJT09hUUpHYmFRYkxhbWlrMEE3ZXNBYkFrZ2xhbUJuQVNrZURQbS9KR2V0NVB0NU5qclJ1CnRKNVh1UUVOQkdaZUIvTUJDQURsZktDc2pPY0JNODhicVEwMUF2Qm9JaHp0U1BJem1iOVpCWkF0dmhBUEx0djcKTEtTbUNzbEl2S29JQWhpU2NyY0F1Z29yanRDcDlrUXpxUlhhWDlnbWFDMDhKZVFxQlNUNjhmbEp0b0tOV1JuSQpFTnZXTFN0azFoeDE5US9NMEQ0S1pDNnRDdVJEcWxVVGVVdlAyc05iNk5TSmJhdlVyNEVoZWZOUFdxTGdvdmRaCmlTL3JrRG01UFNzdXpVSHc2N3NGTEh4Mm1wb3g3MVB4MkhYQ1FKZTl4UitDRkpjUVRnSlJ5WHBaWUFqazhpRUUKK1EyVm9ydXpBYUc0ME9wdDU1MmV4aXgzRzhpSnI2NEE2b0FQRGl3ZXVScTFmYTN6QXlwOWh4d1dXaWhWWW1hNApUOXBIZ0NXSUZKeUpsYUMwQ25HVXBZNm1uOHY5TTF4YUtrc0dYOStKQUJFQkFBR0pBVFlFR0FFSUFDQVdJUVNRCnZkMjdoand1UkZteis2NjdNWjlXQnhXdkVBVUNabDRIOHdJYkRBQUtDUkM3TVo5V0J4V3ZFTjlTQi85SExQMW0KSnJVNEQrQW52NVVaYjRMck5PZjVqcmwrYVVNTFNCOGNFVTN6RU1zL2V0Ykk3SHFqSFpnQjFrMnZwQUpWRUJaWgpxWmJnSEdoRXdxcDRkSjVuMjBTYnVrUlA0VEczSm1kOVRpV3BmaXZyL1puaWtDNnR1Mkd5dzFtclFVWUMxZHJ6CkVPMnZGVDZPS0tKeFZXSmtSVGxLYkRVSEdFa0IwTTBBNVRya0pvbjFBNnJWOXlPMStUcE9IdHBPREJPZFYzZG8KUXNpTWp1S0c4NW5oZFVvWmV2OWhVeGM0VHg0OTdLSng0dmVXbGpJRGFFK3hhM0Nnb1Q3dkNEK2xtQnpwc1Z6MQpmM0ozQWFkYVF0OWd6WDI5RUFsK0lXYnVTd3QwK1hxWnBuT1hscEhaNnNKSGZkazVXWEhBcm5udjRCZ2dhQ3E5CmFLczg5N1RNZVNZck9JTzEKPStoVmMKLS0tLS1FTkQgUEdQIFBVQkxJQyBLRVkgQkxPQ0stLS0tLQo=

Auth-Token: TokenHere
Content-Type: application/json

{"name": "Sam"}
```

Or without body/headers:

```
HLN/1.0 READ /hello-world

LS0tLS1CRUdJTiBQR1AgUFVCTElDIEtFWSBCTE9DSy0tLS0tCgptUUVOQkdaZUIvTUJDQURjS3RoeFZHWTZ2YXNOZ09Dby93c0RHY2tsb2hPZmJFUmorUlpvOXgzUDZaZ3JiMVhGCkVrcUpacHExbWgrRTlQOXVzeGQyYXVYankrbTJVL3RUN25GR0hZOHF0WHEvemxsVjZrS3pWKzNkdGNJNlpSUGUKVkJUZjRtTThhSGQ5S2hVTWVKbXNDL2YxWGJCTzF0djlWS2dkc3dLY0pQdEdsVlFOeWRRaktSNWlieEZuVEdGNAplaGZwajljWVpmc1RzM2oxL2Q0ZU5FUW9OMWRaM2o2bVAwZlJJM2o5VmVGdXNCKzdPSW0vMVFCS0FqMTIxY1VtCjhWb2J1NVNkNm5YaG85NTQ2WFFiRDd1NFl1U25McUpJT2JXUXQzS0ptamJKL212TEFJTGF6VkFWeEEyd1gyMC8KdUlPTDJyNVRUSWFjWVZ3TlhuUkJvbVVyVDVFdE45ZlpxZSszQUJFQkFBRzBEVWh2Ykc5dVpYUkRiR2xsYm5TSgpBVkVFRXdFSUFEc1dJUVNRdmQyN2hqd3VSRm16KzY2N01aOVdCeFd2RUFVQ1psNEg4d0liQXdVTENRZ0hBZ0lpCkFnWVZDZ2tJQ3dJRUZnSURBUUllQndJWGdBQUtDUkM3TVo5V0J4V3ZFTjVKQi85ZVl2bG1OTjExcUhwaHBuM1EKVVpqNkxuZXU5OEtqWTBhY0hkOVZwQk5FOU81T1BXa3VJTlc0TndtaWRCOFRaYkcvNFNhYUIzMG5zYjJudnNPQwpSMTVzNytZRDlrODY3Z0N3d1lEaVczejNrMlVqT2hSWWVVTGI3c3Zqd0oydlVObllKMmtSTFB2czNuOWFxdTErCjhlTGJtd01MMXdRaC81UHlaSlIyZTNSZWtJM0hacldmTzllcmlVTk9zb2tuazNBV2NnMHo5dFY2eTZLVUdmZUgKS0RqamxackkxR2t4ZWdmR0krUGRjNnlBS0lwaXZNM21Ja3RSNGN1UzRtNWFZT2dCR0J5bW9PQ1Zadk81Z3piZQpMenlndHlWZDhNWXFJT09hUUpHYmFRYkxhbWlrMEE3ZXNBYkFrZ2xhbUJuQVNrZURQbS9KR2V0NVB0NU5qclJ1CnRKNVh1UUVOQkdaZUIvTUJDQURsZktDc2pPY0JNODhicVEwMUF2Qm9JaHp0U1BJem1iOVpCWkF0dmhBUEx0djcKTEtTbUNzbEl2S29JQWhpU2NyY0F1Z29yanRDcDlrUXpxUlhhWDlnbWFDMDhKZVFxQlNUNjhmbEp0b0tOV1JuSQpFTnZXTFN0azFoeDE5US9NMEQ0S1pDNnRDdVJEcWxVVGVVdlAyc05iNk5TSmJhdlVyNEVoZWZOUFdxTGdvdmRaCmlTL3JrRG01UFNzdXpVSHc2N3NGTEh4Mm1wb3g3MVB4MkhYQ1FKZTl4UitDRkpjUVRnSlJ5WHBaWUFqazhpRUUKK1EyVm9ydXpBYUc0ME9wdDU1MmV4aXgzRzhpSnI2NEE2b0FQRGl3ZXVScTFmYTN6QXlwOWh4d1dXaWhWWW1hNApUOXBIZ0NXSUZKeUpsYUMwQ25HVXBZNm1uOHY5TTF4YUtrc0dYOStKQUJFQkFBR0pBVFlFR0FFSUFDQVdJUVNRCnZkMjdoand1UkZteis2NjdNWjlXQnhXdkVBVUNabDRIOHdJYkRBQUtDUkM3TVo5V0J4V3ZFTjlTQi85SExQMW0KSnJVNEQrQW52NVVaYjRMck5PZjVqcmwrYVVNTFNCOGNFVTN6RU1zL2V0Ykk3SHFqSFpnQjFrMnZwQUpWRUJaWgpxWmJnSEdoRXdxcDRkSjVuMjBTYnVrUlA0VEczSm1kOVRpV3BmaXZyL1puaWtDNnR1Mkd5dzFtclFVWUMxZHJ6CkVPMnZGVDZPS0tKeFZXSmtSVGxLYkRVSEdFa0IwTTBBNVRya0pvbjFBNnJWOXlPMStUcE9IdHBPREJPZFYzZG8KUXNpTWp1S0c4NW5oZFVvWmV2OWhVeGM0VHg0OTdLSng0dmVXbGpJRGFFK3hhM0Nnb1Q3dkNEK2xtQnpwc1Z6MQpmM0ozQWFkYVF0OWd6WDI5RUFsK0lXYnVTd3QwK1hxWnBuT1hscEhaNnNKSGZkazVXWEhBcm5udjRCZ2dhQ3E5CmFLczg5N1RNZVNZck9JTzEKPStoVmMKLS0tLS1FTkQgUEdQIFBVQkxJQyBLRVkgQkxPQ0stLS0tLQo=





```

### Response
```
HLN/1.0 200 OK

LS0tLS1CRUdJTiBQR1AgUFVCTElDIEtFWSBCTE9DSy0tLS0tCgptUUVOQkdaZUI2SUJDQUNwUlpvNnppMTFxNVRyTlp2QjRKY2EyMEJCRm8zWDhRbHh3OXdmQnN6cmFvd0lWOW1rCmxRVGVXczhUdU5iTWlud25tem1IM0VVOFFOTEY1elJkcGhvelFUNnFKdXRDbTFwcWlPSXJ5YmpuN014cW40QVQKSG5OQW5LSG5NMnVKT0ZjVnN2eEt1Z2JBTmFVenFHWFBzajdBdU9HbzhWM0hsNHJldkZUdVBpWmFnLzdyWE1tVApFOWxHLzRpVDhBcUJoSytvMVhWOXpweTZaOWIzZm1tQUF2elBrYW53VWFlYkhQanlRTEsyRTFzdEh5NnFUbXUzCkVSa1p4NEd4eGxWdUNGY0lHM3VoczBPUUpqZWhDaXo5MG15R0NuTkxXbUl6L0lodTg0ZFN5a2hZZlA4cSt2WmIKQ0tXV3hHSEw4MXQ3cVZ0Y1NMTGtuT2JnWnJKQ2tZT05wMzZwQUJFQkFBRzBEVWh2Ykc5dVpYUlRaWEoyWlhLSgpBVkVFRXdFSUFEc1dJUVJ3K1B0WnZ2VFp0UEd4R0NvVHEvVzRxZU9oOXdVQ1psNEhvZ0liQXdVTENRZ0hBZ0lpCkFnWVZDZ2tJQ3dJRUZnSURBUUllQndJWGdBQUtDUkFUcS9XNHFlT2g5MW5vQi85cmRldG1CZDM0MS9PamROVFkKeW1pSFJZU3VzZmFhZTJUaXAxTUYyNm04Z2pObGhmbUtHQWQ3TUx6WE5vVTNSTEVVanZycHNpZURGUFpqWkI5bApqL2l3d0JoR3NUT1NYdjMzU0Y2ZWZCejZpRVpLVDI4Y00ybFp4ZFIrSTd1STBqRTIzbVZzQVZJbXVuZ2Y3QzVUCmxCYTRMWTdXV2sxT2t3RG9iVDA4d21YbTdyQk05a3pyQXUwRkF1N0RlV053djJBa1F4VTl3STJ3K2E2TEh5M2YKVFZQaUs0dTlRZ3BtUFFrZU5LOXVETHo0ZDNsc2RuVHJra3J1VndTZ2E0djZ2WlAzbTIwZnZVaXlRa0tHL3NWNwpDaUJGUUh5aUoxOEsyS2JBaWdPRHZ4SlJKWFgzWm14TlFSZktwVUU5Z0twWTB5TktNbVNROU91c2JlMG13em1DCjBGRHN1UUVOQkdaZUI2SUJDQURZbW4vbEtzOWFmLzdCRmlLYVY0NG1TQmpQdFgrblFwSjlUMTlsN1ZCTWRlTUwKTTFXek5yTUhuS096WHRsZXpTOGh2bDBSdkw5VWJySzVpRHNqUXhmZmpHSmE2NzZSRHA1TlhwT0Q1eUZaNyt6QQpCK2hESXNJMzlWRXhpOE5RWXdhNFZWSE90eDRRY0hDN2JPZXBEMEI2UG5zNXNvN09PTWgvS2dNRjhtL1ZRVDdmCk94V1htdW4wd1ArVjhDYVdyeVdra1liZlZHUkNDRHVnVHFKeUg2a25iVzVTVUIrMmF2UjNBSW5qYmx2Z2R3RDIKOExJMndIY1Q3N2FTS0NmMmdVelZndEMvWTVtM283S1IvNmtMdTBSNTlKcWl6eXhRRlNCdHNnZnBEOUQ2dnhpMgowbVRiUFhOOHpYaE9Fd3QvRGdmMjhTb2sxTkhjaWRGLy94Vzc5MHJ4QUJFQkFBR0pBVFlFR0FFSUFDQVdJUVJ3CitQdFp2dlRadFBHeEdDb1RxL1c0cWVPaDl3VUNabDRIb2dJYkRBQUtDUkFUcS9XNHFlT2g5OGJ6Qi8wWW02NVUKalFoektGLzlCU1d5VFlYeXhuaVhZSTcxeUZBczk5dTBIK2thVUpJMkphbW5ZcVJINU9WWG9VUzhZZzJnaWR6MApDQmNVQUZWeFVEeElOdkt6WFFrN2MwWko3SnMyNHpUWGxZS3RNNlhUeERRVzBnUmRvenh6clJzYTBldUg5Q1JOCkFxOFBidVFrQnU0SEhOSjduVytoZkRERkg2RjA1eDFaZVo4NU9Ca0RlWGhtNVlON3UvNG5TU1pQcnh3dDVpRFUKZ0ZRWFFNUktIdHBMQTBtVTYrRmh0cXlXMUJQb2xwMmxncmNTSGsrZ2JGTmFTS0s1bjY2ZWNFQnczc0Z3M09PZQp5SHlkT1ZkNmxsZnFKWHhpY1RGQjNraGd5NVVYTExZTGJQZGNnN3FpNWYyNmtMN2ZLTmNFWFBXcWd1MU54OHkrClBBaGpGVURFMVFmaTZuZHgKPW9acHoKLS0tLS1FTkQgUEdQIFBVQkxJQyBLRVkgQkxPQ0stLS0tLQo=

Content-Type: text/plain

Welcome to HoloNet!
```

### Implementation

See the folder `python-example`

---

## 5. Security Considerations

HoloNet is designed to be used with GPG. HoloNet requests and responses are always fully encrypted and signed with GPG, however it is not required.  Servers can accept unencrypted requests, and clients can accept unencrypted responses. As such the GPG Public Key can be left out if desired, in a future version it might be moved to a request/response header for better distinction between encrypted HoloNet and unencrypted HoloNet.

To securely exchange GPG keys from server to client on first request, there are various options:

- Create a trusted centralized key server whose public key is well-known by clients. This central server holds the public key for other servers, clients can fetch and cache these keys when needed.
- Secure HoloNet with TLS, though not explicitly defined clients and server can implement this if desired. You can even forego GPG if TLS meets your needs.
- Run HoloNet in a private trusted network, where MITM attacks are unlikely (i.e. private networks, either with VPN or airgap).
- Serve the server public key out of band, for example via HTTPS. Have client fetch the key from https://server:443/holonet-key and then change protocols. This requires the server and client to understand HTTPS.

---

## 6. References

No references.

---

This RFC outlines the basic structure and functionality of the HoloNet protocol (HLN/1.0), providing a simple and lightweight communication method for client-server interactions. Future versions may expand on this foundation with additional features and improvements.
