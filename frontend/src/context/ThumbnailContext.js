import { createContext, useContext } from 'react';

export const ThumbnailContext = createContext();

export const useThumbnail = () => useContext(ThumbnailContext);