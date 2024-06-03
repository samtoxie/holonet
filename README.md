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

The HoloNet (HLN) protocol is a lightweight, text-based protocol designed for simple client-server communication. It is similar to HTTP but simplified for ease of implementation and use in lightweight applications.

---

## 2. Terminology

- **Client**: The entity that initiates a request to the server.
- **Server**: The entity that processes the request and returns a response.
- **Request Line**: The first line of the request message, containing the method, resource, and protocol version.
- **Status Line**: The first line of the response message, containing the protocol version, status code, and status message.
- **Headers**: Key-value pairs that provide additional information about the request or response.
- **Body**: Optional data sent after the headers in a request or response.

---

## 3. HoloNet Protocol Specification

### 3.1 Request Format

A HoloNet request consists of a request line, optional headers, and an optional body. The format is as follows:

```
HLN <method> <resource> HLN/1.0
<Header-Key>: <Header-Value>
...
<empty line>
<optional body>
```

- **Request Line**: 
  - `<method>`: The action to be performed (e.g., READ, WRITE).
  - `<resource>`: The target resource (e.g., / or /resource-name).
  - `HLN/1.0`: The version of the HoloNet protocol.

- **Headers**: 
  - Each header is a key-value pair separated by a colon and space.

- **Body**: 
  - The body is optional and follows an empty line after the headers.

### 3.2 Response Format

A HoloNet response consists of a status line, optional headers, and an optional body. The format is as follows:

```
HLN/1.0 <status_code> <status_message>
<Header-Key>: <Header-Value>
...
<empty line>
<optional body>
```


- **Status Line**: 
  - `HLN/1.0`: The version of the HoloNet protocol.
  - `<status_code>`: A three-digit number indicating the result of the request (e.g., 200, 404).
  - `<status_message>`: A textual description of the status code (e.g., OK, Not Found).

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
HLN READ / HLN/1.0
Content-Length: 0
```

### Response
```
HLN/1.0 200 OK
Content-Type: text/plain

Welcome to HoloNet!
```

### Implementation

See the folder `python-example`

---

## 5. Security Considerations

HoloNet does not provide built-in security features such as encryption or authentication. It is recommended to use HoloNet over secure channels (e.g., TLS) to ensure the confidentiality and integrity of the data.

---

## 6. References

No references.

---

This RFC outlines the basic structure and functionality of the HoloNet protocol (HLN/1.0), providing a simple and lightweight communication method for client-server interactions. Future versions may expand on this foundation with additional features and improvements.
