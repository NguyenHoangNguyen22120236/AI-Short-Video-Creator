import { jwtDecode } from 'jwt-decode';

export function isTokenValid(token) {
  try {
    const decoded = jwtDecode(token);
    const now = Math.floor(Date.now() / 1000);
    return decoded.exp && decoded.exp > now;
  } catch (e) {
    return false;
  }
}