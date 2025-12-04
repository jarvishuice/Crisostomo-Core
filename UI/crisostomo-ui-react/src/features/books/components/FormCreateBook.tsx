import React, { useState } from "react";

interface BookFormData {
  code: string;
  name: string;
  description: string;
  knowledge_area: string;
  sub_area: string;
  category: string;
  editorial_code: string;
  author: string;
}

export const CreateBookForm: React.FC = () => {
  const [form, setForm] = useState<BookFormData>({
    code: "",
    name: "",
    description: "",
    knowledge_area: "",
    sub_area: "",
    category: "",
    editorial_code: "",
    author: "",
  });
  const [pdfFile, setPdfFile] = useState<File | null>(null);

  // Manejador para cuando el usuario selecciona un archivo
  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setPdfFile(event.target.files[0]);
    }
  };

  // Estos vendrán luego de tus servicios
  const [knowledgeAreas, setKnowledgeAreas] = useState<any[]>([]);
  // SUB ÁREAS
  const [subAreas, setSubAreas] = useState<any[]>([]);
  const [loadingSubAreas, setLoadingSubAreas] = useState<boolean>(false);
// Estado para categorías
const [categories, setCategories] = useState<any[]>([]);
const [loadingCategories, setLoadingCategories] = useState<boolean>(false);
const [editorials, setEditorials] = useState<any[]>([]);
const [authors, setAuthors] = useState<any[]>([]);
  console.log(loadingCategories)
  console.log(loadingSubAreas)
  const handleChange = (e: any) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };
 // Cargar ÁREAS DE CONOCIMIENTO
 React.useEffect(() => {
    const loadKnowledgeAreas = async () => {
      try {
        const res = await fetch("http://localhost:1708/category/areas");
        const data = await res.json();
        setKnowledgeAreas(data);
      } catch (err) {
        console.error("Error cargando áreas:", err);
      } 
    };

    loadKnowledgeAreas();
  }, []);
  
// Cargar SUB-ÁREAS cuando cambie knowledge_area
React.useEffect(() => {
    if (!form.knowledge_area) {
      setSubAreas([]);
      return;
    }

    const loadSubAreas = async () => {
      setLoadingSubAreas(true);
      try {
        const res = await fetch(
          `http://localhost:1708/category/filter/${form.knowledge_area}`
        );
        const data = await res.json();
        setSubAreas(data);
      } catch (err) {
        console.error("Error cargando sub áreas:", err);
      } finally {
        setLoadingSubAreas(false);
      }
    };

    loadSubAreas();
  }, [form.knowledge_area]);


// Cargar categorías cuando cambie la sub área
React.useEffect(() => {
    if (!form.sub_area) {
      setCategories([]);
      return;
    }
  
    const loadCategories = async () => {
      setLoadingCategories(true);
      try {
        // Suponiendo que el endpoint es el mismo que para subáreas
        // y recibe el código de la subárea para filtrar
        const res = await fetch(`http://localhost:1708/category/filter/${form.sub_area}`);
        const data = await res.json();
        setCategories(data);
      } catch (err) {
        console.error("Error cargando categorías:", err);
      } finally {
        setLoadingCategories(false);
      }
    };
  
    loadCategories();
  }, [form.sub_area]);
// Cargar editoriales al montar el componente
React.useEffect(() => {
    const loadEditorials = async () => {
      try {
        const res = await fetch("http://localhost:1708/editorial/");
        const data = await res.json();
        setEditorials(data);
      } catch (err) {
        console.error("Error cargando editoriales:", err);
      }
    };
  
    loadEditorials();
  }, []);


  // Cargar autores al montar el componente
React.useEffect(() => {
    const loadAuthors = async () => {
      try {
        const res = await fetch("http://localhost:1708/author/");
        const data = await res.json();
        setAuthors(data);
      } catch (err) {
        console.error("Error cargando autores:", err);
      }
    };
  
    loadAuthors();
  }, []);
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
  
    if (!pdfFile) {
      alert("Por favor selecciona un archivo PDF.");
      return;
    }
  
    const payload = new FormData();
    // Agregamos los datos del libro como JSON
    payload.append(
      "book",
      JSON.stringify({
        ...form,
        code: "el codigo lo intentará el sistema",
        uploaded_by: "cc2206288ad241eab7308fc3f257f2c7",
        created_at: new Date().toISOString(),
        process_img: false,
      })
    );
    // Agregamos el PDF
    payload.append("pdf_file", pdfFile);
  
    try {
      const res = await fetch("http://localhost:1708/book/", {
        method: "POST",
        body: payload, // multipart/form-data se detecta automáticamente
      });
  
      if (res.status === 201) {
        alert("Libro creado con éxito");
        // Opcional: resetear formulario
        setForm({
          code: "",
          name: "",
          description: "",
          knowledge_area: "",
          sub_area: "",
          category: "",
          editorial_code: "",
          author: "",
        });
        setPdfFile(null);
      } else {
        const errorData = await res.json();
        console.error(errorData);
        alert("Error al crear libro: " + JSON.stringify(errorData));
      }
    } catch (error) {
      console.error(error);
      alert("Error en la conexión: " + error);
    }
  };
  return (
    <div className=" px-6 py-10" style={{minWidth:screen.width * 0.70}}>
      <h2 className="text-3xl font-bold mb-8 text-gray-700">
        Pubicar Libro
      </h2>

      <form 
        onSubmit={handleSubmit}
        className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full"
      >

        {/* Código */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Código</label>
          <input
            type="text"
            name="code"
            value={form.code}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          />
        </div>

        {/* Nombre */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Nombre</label>
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          />
        </div>

        {/* Descripción (full width) */}
        <div className="flex flex-col md:col-span-2">
          <label className="mb-1 font-medium">Descripción</label>
          <textarea
            name="description"
            value={form.description}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
            rows={3}
          ></textarea>
        </div>

        {/* Área conocimiento */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Área de Conocimiento</label>
          <select
            name="knowledge_area"
            value={form.knowledge_area}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            {knowledgeAreas.map((x: any) => (
             <option key={x.cod} value={x.cod}>{x.name}</option>
            ))}
          </select>
        </div>

        {/* Sub área */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Sub Área</label>
          <select
            name="sub_area"
            value={form.sub_area}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            {subAreas.map((x: any) => (
              <option key={x.cod} value={x.cod}>{x.name}</option>
            ))}
          </select>
        </div>

        {/* Categoría */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Categoría</label>
          <select
            name="category"
            value={form.category}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            {categories.map((x: any) => (
              <option key={x.cod} value={x.cod}>{x.name}</option>
            ))}
          </select>
        </div>

        {/* Editorial */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Editorial</label>
          <select
            name="editorial_code"
            value={form.editorial_code}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            {editorials.map((x: any) => (
              <option key={x.code} value={x.code}>{x.name}</option>
            ))}
          </select>
        </div>

        {/* Autor */}
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Autor</label>
          <select
            name="author"
            value={form.author}
            onChange={handleChange}
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            {authors.map((x: any) => (
              <option key={x.cod} value={x.cod}>{x.name}</option>
            ))}
          </select>
        </div>
        <div className="flex flex-col">
  <label className="mb-1 font-medium">Archivo PDF</label>
  <input
    type="file"
    accept="application/pdf"
    name="pdfFile"
    onChange={handleFileChange} // manejador que vamos a crear
    className="border rounded px-3 py-2 w-full"
  />
   {pdfFile && <p className="mt-2 text-sm text-gray-600">Archivo seleccionado: {pdfFile.name}</p>}
</div>

        {/* Botón enviar (full width) */}
        <div className="md:col-span-2">
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-3 rounded-lg text-lg font-semibold hover:bg-blue-700"
          >
            Crear Libro
          </button>
        </div>

      </form>
    </div>
  );
};