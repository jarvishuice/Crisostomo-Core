import React from "react";
import { Link } from "react-router-dom";
import { API_URL } from "../../global/globalValues";

export const Sidebar: React.FC = () => {
    return (
        <aside className="w-60 bg-jenkins-dark border-r border-gray-300 h-screen fixed top-0 left-0 pt-16">
             
            <ul className="p-4 space-y-2 text-sm">
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/dashboard">Dashboard</Link>
                </li>
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/books">Books</Link>
                </li>
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/categories">Categories</Link>
                </li>
                <li>
                    <Link className="block px-3 py-2 hover:bg-gray-300 rounded" to="/authors">Authors</Link>
                </li>
            </ul>
        </aside>
    );
};
