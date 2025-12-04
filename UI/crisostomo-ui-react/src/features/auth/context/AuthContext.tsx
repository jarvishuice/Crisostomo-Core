// import React, { createContext, useState, useEffect } from "react";

// interface AuthContextType {
//     token: string | null;
//     isAuthenticated: boolean;
//     login: (token: string) => void;
//     logout: () => void;
// }

// export const AuthContext = createContext<AuthContextType>({
//     token: null,
//     isAuthenticated: false,
//     login: () => {},
//     logout: () => {},
// });

// export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
//     const [token, setToken] = useState<string | null>(null);

//     useEffect(() => {
//         const storedToken = localStorage.getItem("token");
//         if (storedToken) {
//             setToken(storedToken);
//         }
//     }, []);

//     const login = (token: string) => {
//         localStorage.setItem("token", token);
//         setToken(token);
//     };

//     const logout = () => {
//         localStorage.removeItem("token");
//         setToken(null);
//     };

//     return (
//         <AuthContext.Provider
//             value={{
//                 token,
//                 isAuthenticated: !!token,
//                 login,
//                 logout,
//             }}
//         >
//             {children}
//         </AuthContext.Provider>
//     );
// };
import React, { createContext, useState, useEffect } from "react";

interface UserData {
    username: string;
    email: string;
    full_name: string;
    age: number;
    cod: string;
    birth_date: string;
}

interface AuthContextType {
    token: string | null;
    isAuthenticated: boolean;
    user: UserData | null;
    login: (token: string) => Promise<void>;
    logout: () => void;
}

export const AuthContext = createContext<AuthContextType>({
    token: null,
    isAuthenticated: false,
    user: null,
    login: async () => {},
    logout: () => {},
});

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [token, setToken] = useState<string | null>(null);
    const [user, setUser] = useState<UserData | null>(null);

    // Cargar datos guardados al iniciar la app
    useEffect(() => {
        const storedToken = localStorage.getItem("token");
        const storedUser = localStorage.getItem("user");

        if (storedToken) {
            setToken(storedToken);
        }

        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }, []);

    // 🔥 Llamar al servicio /AUTH/me
    const fetchUserInfo = async (jwt: string) => {
        try {
            const response = await fetch("http://localhost:1708/AUTH/me", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${jwt}`,
                    "Accept": "application/json",
                },
            });

            if (!response.ok) {
                console.error("Error obteniendo datos del usuario");
                return;
            }

            const result = await response.json();

            // La data viene en result.data
            setUser(result.data);
            localStorage.setItem("user", JSON.stringify(result.data));

        } catch (error) {
            console.error("Error en fetchUserInfo:", error);
        }
    };

    // 🔥 Login → guarda token → obtiene usuario
    const login = async (jwt: string) => {
        localStorage.setItem("token", jwt);
        setToken(jwt);

        await fetchUserInfo(jwt);
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setToken(null);
        setUser(null);
    };

    return (
        <AuthContext.Provider
            value={{
                token,
                isAuthenticated: !!token,
                user,
                login,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
