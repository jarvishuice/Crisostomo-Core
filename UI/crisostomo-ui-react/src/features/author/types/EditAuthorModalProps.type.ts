
export interface EditAuthorModalProps {
    isOpen: boolean;
    author: {
        cod: string;
        name: string;
        description: string;
    } | null;
    onClose: () => void;
    onUpdated: () => void; // refrescar lista
}

