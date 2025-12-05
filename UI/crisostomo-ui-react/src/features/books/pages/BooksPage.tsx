import  { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { ListBookGeneral } from "../../../shared/components/ListBookGeneral";

export function BooksPage() {
    const navigate = useNavigate();
    const [knowledgeAreas, setKnowledgeAreas] = useState<any[]>([]);
    const [knowledgeArea, setKnowledgeArea] = useState<string>(""); 
    const [subAreas, setSubAreas] = useState<any[]>([]);
    const [subArea, setSubArea] = useState<string>(""); 
    const [categories, setCategories] = useState<any[]>([]);
    const [category, setCategory] = useState<string>(""); 
    const [books, setBooks] = useState<any[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [searchText, setSearchText] = useState<string>(""); // 🔹 input de texto

    // Cargar áreas de conocimiento
    useEffect(() => {
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

    // Cargar subáreas según el área seleccionada
    useEffect(() => {
        if (!knowledgeArea) {
            setSubAreas([]);
            setSubArea("");
            return;
        }
        const loadSubAreas = async () => {
            try {
                const res = await fetch(
                    `http://localhost:1708/category/filter/${knowledgeArea}`
                );
                const data = await res.json();
                setSubAreas(data);
            } catch (err) {
                console.error("Error cargando sub áreas:", err);
            }
        };
        loadSubAreas();
    }, [knowledgeArea]);

    // Cargar categorías según subárea seleccionada
    useEffect(() => {
        if (!subArea) {
            setCategories([]);
            setCategory("");
            return;
        }
        const loadCategories = async () => {
            try {
                const res = await fetch(
                    `http://localhost:1708/category/filter/${subArea}`
                );
                const data = await res.json();
                setCategories(data);
            } catch (err) {
                console.error("Error cargando categorías:", err);
            }
        };
        loadCategories();
    }, [subArea]);

    // Fetch de libros según filtros
    const fetchBooks = async () => {
        setLoading(true);
        try {
            let url = "http://localhost:1708/book/?size=100&page=1";

            if (searchText) {
                url = `http://localhost:1708/book/seearch/${searchText}`;
            } else if (category) {
                url = `http://localhost:1708/book/filter/category/${category}`;
            } else if (subArea) {
                url = `http://localhost:1708/book/filter/subarea/${subArea}`;
            } else if (knowledgeArea) {
                url = `http://localhost:1708/book/filter/area/${knowledgeArea}`;
            }

            const res = await fetch(url);
            const data = await res.json();
            setBooks(data);
        } catch (err) {
            console.error("Error al cargar libros:", err);
            setBooks([]);
        } finally {
            setLoading(false);
        }
    };

    // Ejecutar fetch cuando cambie cualquier filtro o búsqueda
    useEffect(() => {
        fetchBooks();
    }, [knowledgeArea, subArea, category, searchText]);

    const handleClick = () => {
        navigate("/addBook");
    };

    return (
        <div
            className="w-100 mt-20 ml-2 p-4 bg-white shadow-md rounded-lg border border-gray-200"
            style={{ width: screen.width * 0.70 }}
        >
            <h3 className="text-3xl font-bold text-gray-800">Libros</h3>

            <div className="mb-4 flex justify-end">
                <button
                    type="button"
                    onClick={handleClick}
                    className="bg-blue-600 text-white px-4 py-2 rounded"
                >
                    Publicar Libro
                </button>
            </div>

            {/* Filtros */}
            <div className="mb-4 flex flex-col md:flex-row md:items-center gap-4">
                {/* Área conocimiento */}
                <div className="flex flex-col w-64">
                    <label className="mb-1 font-medium">Área de Conocimiento</label>
                    <select
                        value={knowledgeArea}
                        onChange={(e) => setKnowledgeArea(e.target.value)}
                        className="border rounded px-3 py-2 w-full"
                    >
                        <option value="">-- Seleccione --</option>
                        {knowledgeAreas.map((x: any) => (
                            <option key={x.cod} value={x.cod}>{x.name}</option>
                        ))}
                    </select>
                </div>

                {/* Subárea */}
                <div className="flex flex-col w-64">
                    <label className="mb-1 font-medium">Sub Área</label>
                    <select
                        value={subArea}
                        onChange={(e) => setSubArea(e.target.value)}
                        className="border rounded px-3 py-2 w-full"
                        disabled={!subAreas.length}
                    >
                        <option value="">-- Seleccione --</option>
                        {subAreas.map((x: any) => (
                            <option key={x.cod} value={x.cod}>{x.name}</option>
                        ))}
                    </select>
                </div>

                {/* Categoría */}
                <div className="flex flex-col w-64">
                    <label className="mb-1 font-medium">Categoría</label>
                    <select
                        value={category}
                        onChange={(e) => setCategory(e.target.value)}
                        className="border rounded px-3 py-2 w-full"
                        disabled={!categories.length}
                    >
                        <option value="">-- Seleccione --</option>
                        {categories.map((x: any) => (
                            <option key={x.cod} value={x.cod}>{x.name}</option>
                        ))}
                    </select>
                </div>

                {/* Búsqueda por texto */}
                <div className="flex flex-col w-64">
                    <label className="mb-1 font-medium">Buscar</label>
                    <input
                        type="text"
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                        placeholder="Escribe para buscar..."
                        className="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>
            </div>

            {/* Lista de libros o mensaje si no hay resultados */}
            {loading ? (
                <p className="text-gray-500">Cargando libros...</p>
            ) : books.length === 0 ? (
                <p className="text-gray-500 text-center mt-4">No se encontraron recursos.</p>
            ) : (
                <ListBookGeneral books={books} loading={loading} />
            )}
        </div>
    );
}
