import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js';
import { getAuth, onAuthStateChanged, createUserWithEmailAndPassword, sendEmailVerification, signInWithEmailAndPassword, setPersistence, browserSessionPersistence, signOut } from 'https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js';


async function readFirebaseConfig() {
    try{
        const response = await fetch('/firebaseConfig.json');
        if(!response.ok){
            throw new Error("");
        }
        const firebaseConfig = await response.json();
        return firebaseConfig;
    }
    catch(error){
        throw error;
    }
}

const firebaseConfig = await readFirebaseConfig();

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

await setPersistence(auth, browserSessionPersistence);
await signOut(auth);

export async function SignIn(email, password){
    console.log('in SignIn');
    try{
        console.log('In try');
        const userCredentials = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredentials.user;
        console.log(`${email},${password}`);
        await sendEmailVerification(user);
        console.log('Verification Done');
    }
    catch(error){
        console.log('In catch');
        console.error(error.code, error.message);
    }
}

export async function LogIn(email, password){
    try{
        const userCredentials = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredentials.user;

        if(user.emailVerified){
            console.log(`${user.email} Logged in`);
        }
        else{
            console.error('Not a proper user');
        }
    }
    catch(error){
        console.log(error.code, error.message);
    }
}

onAuthStateChanged(auth, user => {
    if(user!=null){
        console.log(user.email,'logged in\n');
    }
    else{
        console.log('Null user');
    }
});