import { useParams } from "react-router-dom";
export function ReadBook() {
    const { code,name } = useParams<{ code: string ,name:string}>();
    return (<div className="mt-20">
         <center><label className="mt-20 mb-1 font-medium">{name}</label>
       
        <iframe 
         style={{ width: screen.width * 0.70, height: screen.height * 0.65 }} 
         src={"http://localhost:1708/book/preview-pdf/" + code} />
        </center>
        </div>)


}