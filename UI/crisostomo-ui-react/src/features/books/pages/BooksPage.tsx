
import { BookList } from "../components/BookList";
import { useNavigate } from "react-router-dom";

export function BooksPage(){
    const navigate = useNavigate();

    const handleClick = () => {
      navigate("/addBook"); // ruta a la que quieres ir
    };
    return (<div className="w-100 mt-20 ml-2"style={{width:screen.width * 0.70}}>
      <div className="mb-4 flex justify-end">
       <button

      type="button"
      onClick={handleClick}
      className="bg-blue-600 text-white px-4 py-2 rounded justify-end"
    >
    Publicar Libro
    </button>
    </div>
       <div  className="grid grid-cols-1 md:grid-cols-4 gap-6 w-full"> 
      
       <div className="flex flex-col">
          <label className="mb-1 font-medium">Área de Conocimiento</label>
          <select
            name="knowledge_area"
            
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            
          </select>
        </div>
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Área de Conocimiento</label>
          <select
            name="knowledge_area"
            
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            
          </select>
        </div>
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Área de Conocimiento</label>
          <select
            name="knowledge_area"
            
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            
          </select>
        </div>
        <div className="flex flex-col">
          <label className="mb-1 font-medium">Área de Conocimiento</label>
          <select
            name="knowledge_area"
            
            className="border rounded px-3 py-2 w-full"
          >
            <option value="">Seleccione</option>
            
          </select>
        </div>
       </div>
        <BookList></BookList>
    </div>)
}