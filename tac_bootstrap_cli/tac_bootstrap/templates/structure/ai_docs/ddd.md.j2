# Guía de DDD + Arquitectura Hexagonal

## 🎯 ¿Qué es DDD y Arquitectura Hexagonal?

### Domain-Driven Design (DDD)

Modelar el software basándose en el dominio del negocio real, creando un lenguaje ubicuo compartido entre técnicos y expertos del dominio.

### Arquitectura Hexagonal

Aislar la lógica de negocio de detalles de infraestructura, permitiendo que la tecnología sea intercambiable sin afectar el core del negocio.

### Beneficios Combinados

- **Testeabilidad**: Dominio puro sin dependencias externas
- **Flexibilidad**: Cambiar DB o framework sin reescribir lógica de negocio
- **Mantenibilidad**: Separación clara facilita encontrar y modificar código
- **Escalabilidad**: Bounded contexts pueden convertirse en microservicios

---

## 📊 Tabla de Decisión: ¿Qué Capa Usar?

### Por Tipo de Responsabilidad

| Responsabilidad | Capa | Archivo |
|-----------------|------|---------|
| Reglas de negocio, validaciones del dominio | **Domain** | `domain.md` |
| Orquestar casos de uso, coordinar flujos | **Application** | `application.md` |
| Persistencia, APIs externas, mensajería | **Infrastructure** | `infrastructure.md` |
| Endpoints HTTP, GraphQL, CLI, WebSocket | **Presentation** | `presentation.md` |

### Por Pregunta Clave

| Pregunta | Capa | Archivo |
|----------|------|---------|
| ¿Es una regla de negocio que el experto del dominio conoce? | **Domain** | `domain.md` |
| ¿Coordina múltiples entidades o servicios sin lógica de negocio? | **Application** | `application.md` |
| ¿Interactúa con base de datos, APIs o servicios externos? | **Infrastructure** | `infrastructure.md` |
| ¿Recibe peticiones del mundo exterior? | **Presentation** | `presentation.md` |

---

## 📊 Tabla de Decisión: ¿Qué Componente del Dominio Usar?

### Entidades vs Value Objects vs Aggregates

| Situación | Pregunta Clave | Componente | Ubicación |
|-----------|----------------|------------|-----------|
| Objeto con identidad única que cambia en el tiempo | ¿Necesita ID? ¿Tiene ciclo de vida? | **Entity** | `domain/entities/` |
| Objeto definido por sus atributos, sin identidad | ¿Es inmutable? ¿Se compara por valor? | **Value Object** | `domain/value_objects/` |
| Grupo de entidades con consistencia transaccional | ¿Debe persistirse junto? ¿Tiene raíz? | **Aggregate** | `domain/aggregates/` |
| Algo que ocurrió en el dominio | ¿Es un hecho pasado? ¿Notifica cambios? | **Domain Event** | `domain/events/` |
| Lógica que no pertenece a una entidad específica | ¿Opera sobre múltiples entidades? | **Domain Service** | `domain/services/` |
| Contrato para persistencia | ¿Define cómo guardar/obtener agregados? | **Repository Interface** | `domain/repositories/` |

### Ejemplos Rápidos

| Concepto de Negocio | Componente Correcto | Razón |
|---------------------|---------------------|-------|
| Usuario con ID único | Entity | Tiene identidad, cambia en el tiempo |
| Email, Dirección, Dinero | Value Object | Sin identidad, definido por sus valores |
| Orden con sus líneas | Aggregate | Consistencia transaccional, raíz = Orden |
| "Orden fue creada" | Domain Event | Hecho pasado, notifica otros contextos |
| Calcular precio con descuentos | Domain Service | Lógica que opera sobre múltiples entidades |

---

## 📊 Tabla de Decisión: ¿Qué Componente de Application Usar?

| Situación | Componente | Ubicación |
|-----------|------------|-----------|
| Operación que modifica estado | **Command + Handler** | `application/commands/` |
| Operación de solo lectura | **Query + Handler** | `application/queries/` |
| Flujo complejo con múltiples pasos | **Use Case** | `application/use_cases/` |
| Datos de entrada/salida estructurados | **DTO** | `application/dtos/` |

---

## 📁 Estructura de Bounded Context

```bash
module_name/
├── domain/
│   ├── aggregates/
│   ├── entities/
│   ├── value_objects/
│   ├── events/
│   ├── repositories/
│   ├── services/
│   └── exceptions/
├── application/
│   ├── commands/
│   ├── queries/
│   ├── use_cases/
│   └── dtos/
├── infrastructure/
│   ├── adapters/
│   ├── persistence/
│   ├── messaging/
│   └── config/
└── presentation/
    ├── api/
    ├── graphql/
    ├── grpc/
    ├── cli/
    ├── websocket/
    └── sdk/
```

---

## 📚 Documentación por Capas

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| 🔵 Domain | `domain.md` | Lógica de negocio pura, entidades, value objects, eventos |
| 🟢 Application | `application.md` | Casos de uso, commands, queries, orquestación |
| 🟡 Infrastructure | `infrastructure.md` | Persistencia, APIs externas, mensajería |
| 🟣 Presentation | `presentation.md` | Endpoints HTTP, GraphQL, CLI, WebSocket |

---

## 📈 Flujo de Dependencias

```text
Presentation ──→ Application ──→ Domain
Infrastructure ──→ Application ──→ Domain

✅ Permitido: Capas externas dependen de capas internas
❌ Prohibido: Domain NO puede depender de Application o Infrastructure
```

---

## 🔄 Flujo de una Operación (Ejemplo: Crear Orden)

### Diagrama de Secuencia

```text
┌──────────────┐     ┌─────────────┐     ┌────────────┐     ┌────────────────┐
│ Presentation │     │ Application │     │   Domain   │     │ Infrastructure │
│   (Router)   │     │  (Handler)  │     │ (Aggregate)│     │ (Repository)   │
└──────┬───────┘     └──────┬──────┘     └─────┬──────┘     └───────┬────────┘
       │                    │                  │                    │
       │ POST /orders       │                  │                    │
       │ {customer, items}  │                  │                    │
       │ ──────────────────>│                  │                    │
       │                    │                  │                    │
       │                    │ CreateOrderCmd   │                    │
       │                    │ ────────────────>│                    │
       │                    │                  │                    │
       │                    │                  │ new Order()        │
       │                    │                  │ validate()         │
       │                    │                  │ calculateTotal()   │
       │                    │                  │                    │
       │                    │      Order       │                    │
       │                    │ <────────────────│                    │
       │                    │                  │                    │
       │                    │ save(order)      │                    │
       │                    │ ─────────────────────────────────────>│
       │                    │                  │                    │
       │                    │                  │                    │ INSERT INTO
       │                    │                  │                    │ orders...
       │                    │                  │                    │
       │                    │ OrderId          │                    │
       │                    │ <─────────────────────────────────────│
       │                    │                  │                    │
       │  201 Created       │                  │                    │
       │  {orderId: "123"}  │                  │                    │
       │ <──────────────────│                  │                    │
       │                    │                  │                    │
```

### Flujo Paso a Paso

```text
1. PRESENTATION recibe request HTTP
   └── Valida formato, autenticación, permisos
   └── Convierte JSON → Command/DTO

2. APPLICATION orquesta el caso de uso
   └── NO contiene lógica de negocio
   └── Coordina llamadas a Domain e Infrastructure
   └── Maneja transacciones

3. DOMAIN ejecuta lógica de negocio
   └── Crea/modifica Aggregates
   └── Valida reglas de negocio
   └── Emite Domain Events

4. INFRASTRUCTURE persiste cambios
   └── Implementa Repository interfaces
   └── Traduce Domain → SQL/NoSQL
   └── Publica eventos a message broker
```

### Inversión de Dependencias en Acción

```text
┌─────────────────────────────────────────────────────────────┐
│                        DOMAIN LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  interface OrderRepository:                          │   │
│  │      def save(order: Order) -> OrderId              │   │
│  │      def find_by_id(id: OrderId) -> Order | None    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ implementa
                              │
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  class PostgresOrderRepository(OrderRepository):     │   │
│  │      def save(order: Order) -> OrderId:             │   │
│  │          # INSERT INTO orders...                     │   │
│  │      def find_by_id(id: OrderId) -> Order | None:   │   │
│  │          # SELECT FROM orders WHERE...              │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘

Domain define QUÉ necesita (interface)
Infrastructure define CÓMO lo hace (implementación)
```

---

## ✅ Regla de Oro: Dependencias hacia adentro

| Capa | Puede importar de |
|------|-------------------|
| **Domain** | Nada (solo librerías estándar) |
| **Application** | Domain |
| **Infrastructure** | Application, Domain |
| **Presentation** | Application, Domain, Infrastructure (vía DI) |

---

## 🔍 Señales de Violación de Arquitectura

| Señal | Problema | Solución |
|-------|----------|----------|
| Domain importa de Infrastructure | Dependencia invertida | Crear interface en Domain, implementar en Infrastructure |
| Lógica de negocio en Controller | Falta de capas | Mover a Domain o Application |
| SQL en Application Layer | Acoplamiento a DB | Usar Repository interface |
| DTOs con lógica de negocio | Responsabilidades mezcladas | Mover lógica a Domain |

---

## 📖 Referencias

- **"Domain-Driven Design"** - Eric Evans
- **"Implementing Domain-Driven Design"** - Vaughn Vernon
- **"Clean Architecture"** - Robert C. Martin
- **"Hexagonal Architecture"** - Alistair Cockburn
