import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
import { 
    getAuth, 
    onAuthStateChanged, 
    GoogleAuthProvider, 
    signInWithPopup, 
    setPersistence, 
    browserSessionPersistence, 
    signOut 
} from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js';
import { getFirestore, doc, setDoc, getDoc } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js';

async function readFirebaseConfig() {
    try {
        const response = await fetch('/src/firebaseConfig.json');
        if (!response.ok) {
            throw new Error("Could not fetch firebaseConfig.json. Make sure it's in the /public folder.");
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}

const firebaseConfig = await readFirebaseConfig();
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);

const provider = new GoogleAuthProvider();

await setPersistence(auth, browserSessionPersistence);

//Google Sign-In Function
export async function signInWithGoogle() {
    try {
        await signInWithPopup(auth, provider);
    } catch (error) {
        console.error(error.code, error.message);
        alert(error.message);
    }
}

export async function LogOut() {
    try {
        await signOut(auth);
        console.log('User logged out');
        window.location.href = '/src/login.html';
    } catch (error) {
        console.error('Error logging out:', error);
    }
}

onAuthStateChanged(auth, async (user) => {
    const currentPage = window.location.pathname;
    const protectedPages = {
        'Admin': '/src/admin.html',
        'Professor': '/src/prof.html',
        'T.A': '/src/ta.html'
    };
    const protectedPagePaths = Object.values(protectedPages);

    if (user) {        
        const userDocRef = doc(db, "users", user.uid);
        const userDoc = await getDoc(userDocRef);

        if (userDoc.exists()) {
            const role = userDoc.data().role;
            const targetPage = protectedPages[role]; 

            if (targetPage && currentPage !== targetPage) {
                console.log(`User role is '${role}'. Redirecting to ${targetPage}`);
                window.location.href = targetPage;
            }
        } else {
            console.log('New user detected. Checking for selected role in sessionStorage...');
            const role = sessionStorage.getItem('userRole');

            if (role) {
                console.log(`Saving new user with role: ${role}`);
                await setDoc(userDocRef, {
                    email: user.email,
                    role: role,
                    name: user.displayName
                });
                sessionStorage.removeItem('userRole');
                
                const targetPage = protectedPages[role];
                if (targetPage && currentPage !== targetPage) {
                    window.location.href = targetPage;
                }
            } else {
                console.error('New user logged in, but no role was selected.');
                alert('You are a new user. Please sign up using the "New User" page (signin.html) to select your role first.');
                await signOut(auth);
                window.location.href = '/signin.html';
            }
        }
    } else {
        console.log('User is logged out.');
        if (protectedPagePaths.includes(currentPage)) {
            console.log('Access denied. Redirecting to login.');
            window.location.href = '/login.html';
        }
    }
});