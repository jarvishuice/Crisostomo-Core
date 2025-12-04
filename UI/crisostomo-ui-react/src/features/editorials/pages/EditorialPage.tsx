import React, { useEffect, useState } from "react";

interface Editorial {
  code: string;
  name: string;
  description: string;
  created_at: string;
}

const EditorialesPage: React.FC = () => {
  const [editoriales, setEditoriales] = useState<Editorial[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [submitting, setSubmitting] = useState<boolean>(false);

  // Función para cargar editoriales
  const fetchEditoriales = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:1708/editorial/", {
        headers: { accept: "application/json" },
      });
      const data: Editorial[] = await response.json();
      setEditoriales(data);
    } catch (error) {
      console.error("Error al cargar las editoriales:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEditoriales();
  }, []);

  // Función para crear editorial
  const handleCreateEditorial = async () => {
    if (!name.trim()) {
      alert("El nombre es obligatorio");
      return;
    }
    setSubmitting(true);
    try {
      const response = await fetch("http://localhost:1708/editorial/", {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code: "string", // valor fijo, el backend lo reemplaza
          name,
          description,
          created_at: new Date().toISOString(),
        }),
      });

      if (response.status === 201) {
        alert("Editorial creada exitosamente");
        setShowModal(false);
        setName("");
        setDescription("");
        fetchEditoriales(); // refrescar tabla
      } else {
        const errorData = await response.json();
        console.error("Error al crear editorial:", errorData);
        alert("No se pudo crear la editorial");
      }
    } catch (error) {
      console.error(error);
      alert("No se pudo crear la editorial");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="p-6">
      {/* Botón Registrar Editorial */}
      <div className="mb-4 flex justify-end">
        <button
          className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors"
          onClick={() => setShowModal(true)}
        >
          Registrar Editorial
        </button>
      </div>

      {/* Tabla de Editoriales */}
      <div className="overflow-x-auto bg-white shadow-md rounded-lg border border-gray-200">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Código
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Nombre
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Descripción
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Fecha de Creación
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan={4} className="px-6 py-4 text-center text-gray-500">
                  Cargando...
                </td>
              </tr>
            ) : editoriales.length === 0 ? (
              <tr>
                <td colSpan={4} className="px-6 py-4 text-center text-gray-500">
                  No hay editoriales
                </td>
              </tr>
            ) : (
              editoriales.map((editorial) => (
                <tr key={editorial.code} className="hover:bg-gray-50 transition-colors">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {editorial.code}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                    {editorial.name}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">{editorial.description}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {new Date(editorial.created_at).toLocaleDateString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Modal para crear editorial */}
      {showModal && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="bg-white rounded-lg shadow-lg w-96 p-6 relative">
            <h2 className="text-lg font-semibold mb-4">Registrar Editorial</h2>

            <label className="block mb-2 text-sm font-medium text-gray-700">
              Nombre
            </label>
            <input
              type="text"
              className="w-full mb-4 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <label className="block mb-2 text-sm font-medium text-gray-700">
              Descripción
            </label>
            <textarea
              className="w-full mb-4 px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />

            <div className="flex justify-end gap-2">
              <button
                className="bg-gray-300 hover:bg-gray-400 text-black py-2 px-4 rounded transition-colors"
                onClick={() => setShowModal(false)}
                disabled={submitting}
              >
                Cancelar
              </button>
              <button
                className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded transition-colors"
                onClick={handleCreateEditorial}
                disabled={submitting}
              >
                {submitting ? "Creando..." : "Crear"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default EditorialesPage;
