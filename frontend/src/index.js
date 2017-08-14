import './main.css';
import { Main } from './Main.elm';

var app = Main.fullscreen(localStorage.token || null);

app.ports.storeToken.subscribe(function(token) {
  localStorage.token = token;
});
