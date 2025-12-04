import React, { useEffect, useState } from "react";
import { AuthorList } from "../components/AuthorList";
import type { AuthorCardProps } from "../types/AuthorCardProps.type";


const AuthorsPage: React.FC = () => {
    const [authors, setAuthors] = useState<AuthorCardProps[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // Estado del modal
    const [showModal, setShowModal] = useState(false);

    // Estados del formulario
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");

    const [selectedAuthor, setSelectedAuthor] = useState(null);
const [editOpen, setEditOpen] = useState(false);

const openEdit = (author:any) => {
    setSelectedAuthor(author);
    setEditOpen(true);
};

const closeEdit = () => {
    setEditOpen(false);
    setSelectedAuthor(null);
};


    // Cargar autores desde backend
    const loadAuthors = async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await fetch("http://localhost:1708/author/", {
                method: "GET",
                headers: {
                    Accept: "application/json"
                }
            });

            if (!response.ok) {
                throw new Error("Error al obtener los autores");
            }

            const data = await response.json();
            setAuthors(data);
        } catch (err: any) {
            setError(err.message || "Error desconocido");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadAuthors();
    }, []);

    // Crear autor
    const handleCreateAuthor = async (e: React.FormEvent) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:1708/author/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json"
                },
                body: JSON.stringify({
                    name,
                    description
                })
            });

            if (response.status !== 201) {
                throw new Error("Error al crear el autor");
            }

            // Refrescar tabla
            await loadAuthors();

            // Cerrar modal y limpiar form
            setShowModal(false);
            setName("");
            setDescription("");

        } catch (err: any) {
            alert("No se pudo crear el autor");
            console.error(err);
        }
    };

    return (
        <div className="p-6">
            {/* Título y botón */}
            <div className="flex items-center justify-between mb-6">
                <h1 className="text-3xl font-bold text-gray-800">Autores</h1>

                <button
                    onClick={() => setShowModal(true)}
                    className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded shadow transition-colors"
                >
                    Registrar Autor
                </button>
            </div>

            {/* Cargando */}
            {loading && <p className="text-gray-600">Cargando autores...</p>}

            {/* Error */}
            {error && (
                <p className="text-red-600 text-lg">Error: {error}</p>
            )}

            {/* Lista */}
            {!loading && !error && (
                <AuthorList authors={authors} />
            )}

            {/* --------------------- MODAL --------------------- */}
            {showModal && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">

                    <div className="bg-white p-6 rounded-lg shadow-xl w-96">

                        <h2 className="text-xl font-semibold mb-4 text-gray-800">
                            Registrar Autor
                        </h2>

                        {/* Formulario */}
                        <form onSubmit={handleCreateAuthor} className="space-y-4">
                            
                            <div>
                                <label className="text-sm text-gray-700">Nombre</label>
                                <input
                                    type="text"
                                    value={name}
                                    onChange={e => setName(e.target.value)}
                                    required
                                    className="w-full border rounded px-3 py-2 mt-1"
                                    placeholder="Nombre del autor"
                                />
                            </div>

                            <div>
                                <label className="text-sm text-gray-700">Descripción</label>
                                <textarea
                                    value={description}
                                    onChange={e => setDescription(e.target.value)}
                                    required
                                    className="w-full border rounded px-3 py-2 mt-1"
                                    placeholder="Descripción del autor"
                                />
                            </div>

                            {/* Botones */}
                            <div className="flex justify-end gap-3 mt-4">
                                <button
                                    type="button"
                                    onClick={() => setShowModal(false)}
                                    className="px-4 py-2 bg-gray-300 hover:bg-gray-400 rounded"
                                >
                                    Cancelar
                                </button>

                                <button
                                    type="submit"
                                    className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded"
                                >
                                    Guardar
                                </button>
                            </div>
                        </form>

                    </div>
                </div>
            )}
        </div>
    );
};

export default AuthorsPage;
