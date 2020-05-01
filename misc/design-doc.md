# IOT Platform Design Document

## Definition

While working for The Procter & Gamble Company, Kevin Ashton coined the term Internet of Things. Since then the world has envisioned a future where all devices are interconnected and also available. We try to build a full-fleged IOT platform here which will help high-level software, applications, and systems interact with lower-level protocols, methods of communication, and heterogeneous objects overall.

---

## Scope

As a team of 2 we will be implmenting all aspects of one layer (namely the Device Layer). The rest of the platform will be made using already exisiting tools available on the internet that we will deploy and implement the test applications in. 

In the Device Layer, we will implement 2 parts, the Device Simulator and Device Manager. There can be multiple instances of the device simulator each simulating one or more device. The Manager will act as a gateway which will collate and format the data from all devices. It is also responsible for grouping of the devices into various groups and handling advanced commands.

We will also be making a UI for the manager, where the application developer can see the status of each device and also issue commands. 

The rest of the document specifies the aims of our entire platform made using preexisiting tools available and used by millions of people. 

The completed platform will support processing post network and pre-application, such as system-level protocol decoding, converting, decrypting, and so forth. The platform will control and coordinate protocols and overall communication orchestration. It will also support driver-level logic and the underlying architecture of the overall system that depends on them.

---

## IoT Platform

### System Requirements

Features Requirements

- Scalability: should be reasonably easy to scale the platform without breaking existing functionalities and without disrupting existing production setup.
- Reliability: it is an expectation that anything that forms the core of a solution or product should be reliable.
- Customization: The application developer using the platform should be able to allow customize the parts of the platform they want to use.  
- Supported protocols and interfaces: By fundamental definition, an IoT middleware platform sits between two heterogeneous systems: physical devices and cloud software (and there are umpteen numbers of device types and software). The platform should be able to coordinate with all of them, orchestrate things in unison, and speak all of the languages or protocols.
- Hardware agnostic. The Internet of Things is essentially a group of heterogeneous connected things, hardware devices, computer systems, and software.
- Cloud agnostic: The platform should have no dependency on the cloud.
- Architecture and technology stack. A well-defined architecture and the appropriate combination of the technology stack is a key thing that differentiates a good IoT platform from the others. Need a good combination of a fluid and a rigid architecture backed by a solid, efficient technology stack.
- Security: Security becomes a vital consideration factor if you choose a multitenant platform. The multitenant aspect makes the system more vulnerable, because your own application may be just fine but another application using the same platform (a co-tenant of your application) can create security problems for every other tenant; the risk is always present.

IoT Solution

![Design%20Document%20Scratch/2-1.png](https://github.com/nemaniarjun/IDS/blob/master/2-1.png)

- Devices (a.k.a. “things”) are physical sensors and actuators. They measure various parameters and translate them into electrical or digital data. These sensors are either connected to the host devices (typical for legacy upgrades) or integrated into the host devices (modern). These devices are critical nodes of an IoT application and are required to deliver full-solution functionality by acting as inputs, outputs, or both.
- Gateways are edge devices that can communicate with the upstream system in one of two ways: with or without a gateway. Some devices have the capability to communicate directly over Internet Protocol (IP) using various communication protocols, such as REST, MQTT, AMQP, CoAP, and so forth. In addition to providing a transport mechanism, a gateway can also provide optional functions, such as data segregation, clean up, aggregation, deduplication, and edge computing.
- An IoT platform is the orchestrator of the whole IoT solution and is often hosted in the cloud. This block is responsible for communicating with downstream devices and ingesting large amounts of data at a very high speed. The platform is also responsible for storage of the data in a time series and structured format for further processing and analysis.
- Applications are the front face of the whole solution; it must be presented to the end user in a meaningful way. These applications are desktop based, mobile based, or both. Applications also enrich the data from the platform in various ways and present it to the users in a usable format. Additionally, these applications integrate with other systems and applications at the interface level and enable interapplication data exchange.

---

### System Design

![Design%20Document%20Scratch/2-2.png](https://github.com/nemaniarjun/IDS/blob/master/2-2.png)

Interconnecting arrows indicate the data and information flow between each block. Each block is indicative of the major functional component of the platform. The platform is installed on a virtual cloud machine.

The core functional blocks—the device interface and message broker, the message router and communications module, data storage, device management, and the rule engine are critical for the effective functioning of an IoT platform.

In a nutshell, our platform will be fully functional from the perspective of a core IoT platform. All the aspects that are considered features will be left out for future enhancements. This is a good compromise of speed over features and will in no way harm the product performance of this platform.

---

### Tech Stack

Cloud Instance: Digital Ocean

Operating System: Linux

Web Server: Apache

Database: MySQL

Scripting Language: Python

Flow Editor: Node-RED

---

## Components

### Device Manager

It essentially provides the generic functionality of managing devices as assets. This includes listing all the devices, their active-inactive status, battery levels, network conditions, access keys, readings, stored data access, device details, session information, and other similar things.
The device manager also helps with managing over-the-air updates for a fleet of devices, or central monitoring functions for system admins. In certain use cases, devices also need access rights, and users may be assigned certain access rights to a set of devices. Management of such an accessibility matrix becomes easy with the device manager.

### Test Cases

---

### Edge Interface, Message Broker, and Message Bus
![Pub-Sub Model](https://github.com/nemaniarjun/IDS/blob/master/ias-pub-sub.png)

This module deals and talks with the physical world, especially heterogeneous devices and sensors. This module decouples the entire platform from devices in an effective way. Regardless of the medium of communication, network type used, and protocols in play, the message broker’s job is to consolidate the data in a unified manner and push it to the common message bus. All the other functional blocks share this message bus for further operation. The broker acts as a coordinator and consolidator of messages.

Message brokers are generally middleware programs that provide asynchronous communication abilities to all connected applications and devices, with the help of a publish-subscribe mechanism. It is a broker’s job to receive all the messages from all the clients, filter them, look up which client is subscribed to what topic, and then redistribute the messages to those clients.

It is important that the message broker we select fulfill certain essential criterion. In general, two criterions are important: easy to configure and maintain, and stable enough for the production environment. We will use the MQTT protocol for message exchange because MQTT is almost a de facto protocol for edge devices and IoT applications communication. Mosquitto is a popular open source MQTT implementation, and we will use it to build our message broker.

### Test Cases

---

### Message Router and Communication Management

Once the messages are available on the main message bus, the message may need to include more context or refinement to be useful to other modules. Some messages need feature enrichment and additional information to be appended or added separately, which depends on the context of the device deployment and application requirements. The functionality of enriching existing data messages, rebroadcasting them to the message bus, publishing additional contextual information and other messages after the main message arrives, and tagging them as appropriate is the job of the communication management module. Communication management functions coordinate with the message broker and the rule engine block and interacts with the device manager, as required.

### Test Cases

---

### Time Series Storage and Data Management

As the name suggests, this block stores all the received and parsed data that is available on the message bus in sequential (i.e., time-series style). Very often, communication and routing modules, or the message broker itself, need recent data for specific functional purposes; this storage comes in handy for all such instances.

From a platform’s perspective, we need this storage and retrieval mechanism so that we are able to retrieve data later; and for unsynchronized applications and devices, this data can serve as a shadow copy of the information.

The key question is how we want to store the data. The data that we refer to is transactional data that passes through our message broker and central message bus communication manager. This data has only a few information fields, which are used for data processing and audit purposes, and accordingly, our data storage schema has to be suitable for that.
With MQTT communication, a data packet comes with two fields in each message: topic and payload. The topic typically works as a key for the data, while the payload is actual data or content. Since MQTT is a messaging protocol and does not necessarily specify the format of the payload, we can be flexible.

However, to maintain scalability and a unified approach throughout the platform, we will use JSON (JavaScript Object Notation) encoding for our payload (a.k.a. data packet) throughout the platform.

Schema: ID, Topic, Payload, Timestamp

### Test Cases

---

### Rule Engine

The rule engine is the execution block that monitors the message bus and events across the platform and takes action based on set rules.

The rule engine is constantly listening to the message bus broadcasts. When the communication block puts up a decoded data packet from the downstream device on to the message bus, a rule triggers. The rule engine broadcasts another message (alert) to the message bus. The rule engine also helps with building modular rules for decoding and enriching existing or received data from devices, and therefore, augments the communication module’s functionality.

### Test Cases

---

### The REST API Interface

Restful APIs are useful for support functions and utilities that do not need constant or real-time connectivity and access. Although typically used by upstream programs and applications, downstream devices can also access these APIs when needed.

The REST API works with the message broker and communications manager to present the received data post to the main message bus; it may also use time-series database records to send back the response to the sensor. This response may contain additional information for the sensor to do its job in a certain way for the next round.
This API block can also support data aggregation and bulk operational functionalities, such as querying multiple records by the upstream application. This way, upstream applications and systems remain decoupled from the core platform blocks, thereby maintaining the partition of functions and ensuring security. Various role-based authentications can be built in for access to the API.
The REST API block can also feed into the rule engine and allow applications to configure or trigger specific rules at any given point in time.

With the Mosquitto MQTT broker and the time-series storage in place, our platform will be able to ingest data packets and communicate over MQTT in general. This communication (over MQTT) will be data stream–based and will not necessarily have any built-in intelligence without the rest of the platform.

### Test Cases

---

### Microservices

Besides data management, manipulation, and exchange functionalities, the IoT platform also needs certain support functions to function effectively. Services such as text messaging or email notifications, verifications, captcha, social media authentications, or payment services integration are a few examples of these auxiliary services. These services are bundled in the microservices block.

---

### Application and User Management

Typical user management functions, such as passwords and credentials, access keys, logins, and rights are managed through this block. For upstream applications and various other integrated systems, API keys, credentials, and access can be managed through the same block.

---

## Sample Applications
We will be building the following sample applications:
 - Classroom Management System
 - Smart City Management System

More details are in the TestCases File.
