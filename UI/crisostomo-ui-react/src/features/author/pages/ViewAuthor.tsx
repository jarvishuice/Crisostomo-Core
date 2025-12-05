import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { ListBookGeneral } from "../../../shared/components/ListBookGeneral";
import BackButton from "../../../shared/components/BackButton";

interface Author {
  cod: string;
  name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

const ViewAuthor: React.FC = () => {
  const { cod } = useParams();
  const [author, setAuthor] = useState<Author | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchBooks = async () => {
      const res = await fetch(`http://localhost:1708/book/filter/auhtor/${cod}`);
      setBooks(await res.json());
      setLoading(false);
    };
    fetchBooks();
  }, [cod]);
  
  
  useEffect(() => {
    const fetchAuthor = async () => {
      try {
        const res = await fetch(`http://localhost:1708/author/${cod}`);
        if (!res.ok) throw new Error("Error obteniendo el autor");

        const data = await res.json();
        setAuthor(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAuthor();
  }, [cod]);

  if (loading) return <div className="p-4">Cargando autor...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="max-w-4xl mx-auto mt-15 p-6 bg-white shadow-md rounded-lg border border-gray-200">
      <BackButton to="/authors"/> <center> <h1 className="text-3xl font-bold text-gray-800 mb-4">Detalles del Autor</h1>
   <img
                src={"http://localhost:1708/author/"+cod+"/300/300"}
                
                className=" w-50 h-50 rounded-full border object-cover"
            /></center>
      <div className="space-y-4">

        <div>
          <label className="font-semibold text-gray-600">Código:</label>
          <p className="text-gray-800">{author?.cod}</p>
        </div>

        <div>
          <label className="font-semibold text-gray-600">Nombre:</label>
          <p className="text-xl text-gray-900">{author?.name}</p>
        </div>

        <div>
          <label className="font-semibold text-gray-600">Descripción:</label>
          <p className="text-gray-900 text-justify leading-relaxed">
            {author?.description}
          </p>
        </div>

    

      </div>

     
    <ListBookGeneral books={books} loading={loading} />

  

    </div>
  );
};

export default ViewAuthor;
