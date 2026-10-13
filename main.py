
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API Planes Turísticos - ADSO",
    description="API RESTful para gestionar paquetes turísticos mediante operaciones CRUD",
    version="2.0.0"
)

# Modelo principal: PaqueteTuristico
class PaqueteTuristico(BaseModel):
    id: int
    destino: str
    duracion_dias: int
    precio_por_persona: float
    incluye_tiquetes_aereos: bool

# Modelo para actualizar un paquete turístico
class PaqueteTuristicoUpdate(BaseModel):
    destino: str
    duracion_dias: int
    precio_por_persona: float
    incluye_tiquetes_aereos: bool

# Base de datos simulada en memoria
db_paquetes: List[PaqueteTuristico] = [
    PaqueteTuristico(
        id=1,
        destino="Cartagena",
        duracion_dias=5,
        precio_por_persona=1200000.0,
        incluye_tiquetes_aereos=True
    ),
    PaqueteTuristico(
        id=2,
        destino="Santa Marta",
        duracion_dias=4,
        precio_por_persona=850000.0,
        incluye_tiquetes_aereos=False
    )
]

# 1. READ ALL: Obtener todos los paquetes
@app.get(
    "/api/v1/paquetes",
    response_model=List[PaqueteTuristico],
    status_code=status.HTTP_200_OK
)
def obtener_todos_los_paquetes():
    return db_paquetes

# 2. READ ONE: Obtener un paquete por ID
@app.get(
    "/api/v1/paquetes/{paquete_id}",
    response_model=PaqueteTuristico,
    status_code=status.HTTP_200_OK
)
def obtener_paquete_por_id(paquete_id: int):
    for paquete in db_paquetes:
        if paquete.id == paquete_id:
            return paquete

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El paquete turístico con ID {paquete_id} no existe."
    )

# 3. CREATE: Registrar un nuevo paquete
@app.post(
    "/api/v1/paquetes",
    response_model=PaqueteTuristico,
    status_code=status.HTTP_201_CREATED
)
def crear_nuevo_paquete(paquete: PaqueteTuristico):
    for p in db_paquetes:
        if p.id == paquete.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un paquete turístico con el ID {paquete.id}."
            )

    # Validaciones normales
    if paquete.duracion_dias < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La duración del paquete debe ser como mínimo de 1 día."
        )

    if paquete.precio_por_persona <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El precio por persona debe ser mayor que cero."
        )

    db_paquetes.append(paquete)
    return paquete

# 4. UPDATE: Actualizar un paquete (PUT)
@app.put(
    "/api/v1/paquetes/{paquete_id}",
    response_model=PaqueteTuristico,
    status_code=status.HTTP_200_OK
)
def actualizar_paquete(
    paquete_id: int,
    datos_actualizados: PaqueteTuristicoUpdate
):
    for index, paquete in enumerate(db_paquetes):
        if paquete.id == paquete_id:

            # Validaciones normales
            if datos_actualizados.duracion_dias < 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="La duración del paquete debe ser como mínimo de 1 día."
                )

            if datos_actualizados.precio_por_persona <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio por persona debe ser mayor que cero."
                )

            paquete_modificado = PaqueteTuristico(
                id=paquete_id,
                destino=datos_actualizados.destino,
                duracion_dias=datos_actualizados.duracion_dias,
                precio_por_persona=datos_actualizados.precio_por_persona,
                incluye_tiquetes_aereos=datos_actualizados.incluye_tiquetes_aereos
            )

            db_paquetes[index] = paquete_modificado
            return paquete_modificado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible actualizar. El paquete turístico con ID {paquete_id} no existe."
    )

# 5. DELETE: Eliminar un paquete
@app.delete(
    "/api/v1/paquetes/{paquete_id}",
    status_code=status.HTTP_200_OK
)
def eliminar_paquete(paquete_id: int):
    for index, paquete in enumerate(db_paquetes):
        if paquete.id == paquete_id:
            db_paquetes.pop(index)
            return {
                "mensaje": f"El paquete turístico con ID {paquete_id} fue eliminado exitosamente."
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No es posible eliminar. El paquete turístico con ID {paquete_id} no existe."
    )
