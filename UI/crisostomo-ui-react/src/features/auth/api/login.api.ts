// src/auth/api/loginApi.ts

export const loginRequest = async (username: string, password: string): Promise<string> => {
    const response = await fetch("http://localhost:1708/AUTH/login", {
        method: "POST",
        headers: {
            "accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ username, password })
    });

    if (!response.ok) {
        throw new Error("Credenciales incorrectas");
    }

    const token = await response.text(); // La API devuelve un STRING
    return token;
};
