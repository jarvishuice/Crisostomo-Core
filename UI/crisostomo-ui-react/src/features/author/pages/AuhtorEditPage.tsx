
import React, { useState, useEffect, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";

interface Author {
    cod: string;
    name: string;
    description: string;
}

const AuthorEditPage: React.FC = () => {
    const { cod } = useParams<{ cod: string }>();
    const navigate = useNavigate();

    const [author, setAuthor] = useState<Author | null>(null);
    const [description, setDescription] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [selectedImage, setSelectedImage] = useState<File | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    // Cargar datos del autor
    const loadAuthor = async () => {
        try {
            setLoading(true);
            setError(null);

            const response = await fetch(`http://localhost:1708/author/`);
            if (!response.ok) throw new Error("Error al cargar el autor");

            const data: Author[] = await response.json();
            const selected = data.find(a => a.cod === cod);
            if (!selected) throw new Error("Autor no encontrado");

            setAuthor(selected);
            setDescription(selected.description || "");

        } catch (err: any) {
            setError(err.message || "Error desconocido");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (cod) loadAuthor();
    }, [cod]);

    // Guardar cambios
    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!author) return;

        try {
            // 1️⃣ Actualizar descripción
            const payload = {
                cod: author.cod,
                description: description
            };

            const responseDesc = await fetch("http://localhost:1708/author/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Accept: "application/json"
                },
                body: JSON.stringify(payload)
            });

            if (responseDesc.status !== 201) {
                alert("Error al actualizar la descripción");
                return;
            }

            // 2️⃣ Subir imagen si hay una seleccionada
            if (selectedImage) {
                const formData = new FormData();
                formData.append("file", selectedImage);

                const responseImage = await fetch(
                    `http://localhost:1708/author/upload-image/${author.cod}`,
                    {
                        method: "POST",
                        body: formData
                    }
                );

                if (responseImage.status !== 201) {
                    alert("Error al subir la imagen");
                    return;
                }
            }

            alert("Autor actualizado correctamente");
            navigate("/authors");

        } catch (err) {
            alert("Error de conexión");
            console.error(err);
        }
    };

    // Manejar selección de imagen
    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setSelectedImage(e.target.files[0]);
        }
    };

    if (loading) return <p className="p-6">Cargando autor...</p>;
    if (error) return <p className="p-6 text-red-600">{error}</p>;
    if (!author) return <p className="p-6">Autor no encontrado</p>;

    return (
        <div className="p-6 max-w-md mt-20 mx-auto bg-white shadow-md rounded-lg">
            <h1 className="text-2xl font-bold mb-4">Editar Autor: {author.name}</h1>

            {/* Imagen + Botón cambiar */}
            <div className="flex items-center gap-4 mb-4">
                <div className="relative">
                    <img
                        src={selectedImage ? URL.createObjectURL(selectedImage) : `http://localhost:1708/author/${cod}/300/300`}
                        alt={author.name}
                        className="w-32 h-32 object-cover rounded border"
                    />
                    <button
                        type="button"
                        className="absolute bottom-0 right-0 bg-gray-800 text-white text-xs px-2 py-1 rounded"
                        onClick={() => fileInputRef.current?.click()}
                    >
                        Cambiar
                    </button>
                    <input
                        type="file"
                        ref={fileInputRef}
                        style={{ display: "none" }}
                        accept=".jpg,.jpeg,.png,.gif"
                        onChange={handleImageChange}
                    />
                </div>
            </div>

            <form onSubmit={handleSave} className="flex flex-col gap-4">
                <div>
                    <label className="block text-gray-700">Nombre</label>
                    <input
                        type="text"
                        value={author.name}
                        disabled
                        className="w-full border rounded px-3 py-2 mt-1 bg-gray-100"
                    />
                </div>

                <div>
                    <label className="block text-gray-700">Descripción</label>
                    <textarea
                        value={description}
                        onChange={e => setDescription(e.target.value)}
                        className="w-full border rounded px-3 py-2 mt-1"
                        rows={5}
                    />
                </div>

                <div className="flex justify-end gap-3 mt-4">
                    <button
                        type="button"
                        onClick={() => navigate("/authors")}
                        className="px-4 py-2 bg-gray-400 hover:bg-gray-500 text-white rounded"
                    >
                        Cancelar
                    </button>

                    <button
                        type="submit"
                        className="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded"
                    >
                        Guardar
                    </button>
                </div>
            </form>
        </div>
    );
};

export default AuthorEditPage;
