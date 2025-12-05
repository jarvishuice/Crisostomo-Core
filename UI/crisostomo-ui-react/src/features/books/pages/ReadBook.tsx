import { useParams } from "react-router-dom";
import BackButton from "../../../shared/components/BackButton";
export function ReadBook() {
    const { code,name } = useParams<{ code: string ,name:string}>();
    return (<div className="mt-20 ml-2 p-2  bg-white shadow-md rounded-lg  border-gray-20">
        <BackButton to="/books"/>
         <center><label className="mt-20 mb-1 font-medium">{name}</label>
       
        <iframe 
         style={{ width: screen.width * 0.75, height: screen.height * 0.825 }} 
         src={"http://localhost:1708/book/preview-pdf/" + code} />
        </center>
        </div>)


}