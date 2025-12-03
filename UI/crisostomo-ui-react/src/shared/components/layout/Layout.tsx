import React from "react";
import { Navbar } from "./Navbar";
import { Sidebar } from "./Sidebar";
import { Outlet } from "react-router-dom";

export const Layout: React.FC = () => {
    return (
        <div className="w-100">
             <Sidebar />
            <Navbar />

            <main className="ml-60 mt-16 p-6 w-full bg-[#f4f4f4] min-h-screen">
               <Outlet/>
            </main>
        </div>
    );
};
