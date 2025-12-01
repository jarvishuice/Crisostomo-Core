#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cargar_autores.py
Envía secuencialmente (uno a uno) la lista de autores a POST http://localhost:8000/author/
Cada payload incluye un campo "uuid" generado localmente.
Requisitos:
    pip install aiohttp
Uso:
    python cargar_autores.py
Ajustes: modificar API_URL si tu endpoint es distinto, o añadir Authorization en HEADERS.
"""

import asyncio
import aiohttp
import uuid
import time
import json
from typing import List, Dict

API_URL = "http://localhost:8000/author/"  # ajusta si es necesario
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
REQUEST_TIMEOUT = 15  # segundos

AUTHORS: List[Dict] = [{"name": "Robert C. Martin (Uncle Bob)",
                        "description": "Clean Code; promotor de prácticas de calidad, principios SOLID y del movimiento de desarrollo ágil."},
                       {"name": "Martin Fowler",
                        "description": "Refactoring; autoridad en arquitectura, refactorización y diseño evolutivo."},
                       {"name": "Kent Beck",
                        "description": "Test-Driven Development; creador de Extreme Programming y defensor del TDD."},
                       {"name": "Fred Brooks",
                        "description": "The Mythical Man-Month; análisis clásico sobre gestión de proyectos y complejidad en software."},
                       {"name": "Grady Booch",
                        "description": "Object-Oriented Analysis and Design; contribuciones a UML y diseño orientado a objetos."},
                       {"name": "Eric Evans",
                        "description": "Domain-Driven Design; impulsor del diseño centrado en el dominio para sistemas complejos."},
                       {"name": "Michael Feathers",
                        "description": "Working Effectively with Legacy Code; técnicas para mantener y mejorar código heredado."},
                       {"name": "Steve McConnell",
                        "description": "Code Complete; prácticas pragmáticas para escribir código de alta calidad."},
                       {"name": "Mary Poppendieck",
                        "description": "Lean Software Development; adaptación de principios Lean al desarrollo de software."},
                       {"name": "Tom Poppendieck",
                        "description": "Lean Software Development; coautor en la adaptación de Lean a prácticas de ingeniería de software."},
                       {"name": "Alistair Cockburn",
                        "description": "Agile Software Development; signatario del Manifiesto Ágil y autor sobre métodos ágiles."},
                       {"name": "Ivar Jacobson",
                        "description": "Contribuciones a métodos de desarrollo y UML; enfoque en componentes y casos de uso."},
                       {"name": "Rebecca Wirfs-Brock",
                        "description": "Responsibility-Driven Design; diseño orientado a responsabilidades y patrones de objetos."},
                       {"name": "Martin Kleppmann",
                        "description": "Designing Data-Intensive Applications; diseño de sistemas distribuidos y manejo de datos a escala."},
                       {"name": "Patricia Selinger",
                        "description": "Trabajos en optimización de bases de datos y sistemas de gestión de datos."},
                       {"name": "Ellen Gottesdiener",
                        "description": "Especialista en requisitos ágiles y técnicas de descubrimiento de producto."},
                       {"name": "Gene Kim",
                        "description": "The Phoenix Project; difusión de prácticas DevOps y flujo de trabajo en TI."},
                       {"name": "Jez Humble",
                        "description": "Continuous Delivery; prácticas de entrega continua y despliegue seguro."},
                       {"name": "Nicole Forsgren",
                        "description": "Investigación empírica sobre desempeño de equipos y DevOps (DORA)."},
                       {"name": "Roy Fielding",
                        "description": "REST; definió principios de arquitectura web escalable en su tesis y trabajos."},
                       {"name": "Barbara Liskov",
                        "description": "Principios de diseño de sistemas y tipos abstractos; influencia en diseño de software robusto."},
                       {"name": "David Heinemeier Hansson",
                        "description": "Creador de Ruby on Rails; impacto en productividad y convenciones sobre configuración."},
                       {"name": "Eric S. Raymond",
                        "description": "The Cathedral and the Bazaar; análisis cultural del desarrollo abierto y colaborativo."},
                       {"name": "Sandi Metz",
                        "description": "Prácticas de diseño orientado a objetos y código mantenible, especialmente en Ruby."},
                       {"name": "Addy Osmani",
                        "description": "Optimización web y rendimiento front-end; guías prácticas para aplicaciones modernas."},
                       {"name": "Nicolas Zakas",
                        "description": "Arquitectura y buenas prácticas en JavaScript y front-end a gran escala."},
                       {"name": "John Ousterhout",
                        "description": "A Philosophy of Software Design; enfoque en simplicidad y modularidad en diseño de software."},
                       {"name": "Tom DeMarco",
                        "description": "Peopleware; gestión de equipos y factores humanos en proyectos de software."},
                       {"name": "Steve Blank",
                        "description": "Metodologías de descubrimiento de clientes y validación de producto aplicadas a software."},
                       {"name": "James Rumbaugh",
                        "description": "Coautor de UML; contribuciones al modelado visual y diseño orientado a objetos."}]


async def post_one(session: aiohttp.ClientSession, url: str, payload: Dict) -> Dict:
    start = time.perf_counter()
    try:
        async with session.post(url, json=payload, timeout=REQUEST_TIMEOUT) as resp:
            elapsed = time.perf_counter() - start
            try:
                body = await resp.json()
            except Exception:
                body = await resp.text()
            return {"status": resp.status, "ok": 200 <= resp.status < 300, "elapsed": elapsed, "body": body}
    except Exception as e:
        return {"status": None, "ok": False, "elapsed": time.perf_counter() - start, "body": str(e)}


async def main():
    created = []
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        for author in AUTHORS:
            payload = dict(author)
            payload["uuid"] = str(uuid.uuid4())
            res = await post_one(session, API_URL, payload)
            created.append({
                "name": payload["name"],
                "uuid": payload["uuid"],
                "status": res["status"],
                "ok": res["ok"],
                "elapsed": res["elapsed"],
                "response": res["body"]
            })
            print(f"POST {payload['name'][:40]:40} -> status={res['status']} ok={res['ok']} time={res['elapsed']:.3f}s")
    # Guardar resumen en archivo JSON
    with open("created_authors_summary.json", "w", encoding="utf-8") as f:
        json.dump(created, f, ensure_ascii=False, indent=2)
    print(f"\nCarga finalizada. Resumen guardado en created_authors_summary.json ({len(created)} items).")


if __name__ == "__main__":
    asyncio.run(main())
