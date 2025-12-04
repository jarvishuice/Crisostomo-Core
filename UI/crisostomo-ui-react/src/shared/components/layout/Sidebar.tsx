import React, { useContext } from "react";
import { Link } from "react-router-dom";
import Logo from "../../../assets/logo.png"
import { AuthContext } from "../../../features/auth/context/AuthContext";
import { API_URL } from "../../global/globalValues";
export const Sidebar: React.FC = () => {
    const { user } = useContext(AuthContext);
    return (
        <aside className="w-60 bg-jenkins-dark border-r border-gray-300 h-screen fixed top-0 left-0 pt-16">
            <center><img 
    src={API_URL + "/users/profile/picture/" + user?.cod + "/300/300"}  
    className="w-40 h-40 mt-3 rounded-full border"
    alt="Foto de perfil del usuario"
    onError={(e) => {
        // En React usamos e.currentTarget para acceder al elemento DOM
        e.currentTarget.onerror = null; // Previene el bucle infinito
        e.currentTarget.src = Logo; // Cambia a la imagen por defecto
    }}
/> </center>
            <center><span className="inline-block max-w-[150px] truncate font-bold"
                title="@user?.full_name">{user?.full_name.toUpperCase()}</span></center>
            <center> <small>{user?.username.toUpperCase()}</small></center>
            <hr className="border-t border-gray-300 my-4" />

            <ul className="p-4 space-y-2 text-sm">
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/books">Libros</Link>
                </li>
            
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/authors">Autores</Link>
                </li>
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/editorials">Editorial</Link>
                </li>
            </ul>
        </aside>
    );
};
