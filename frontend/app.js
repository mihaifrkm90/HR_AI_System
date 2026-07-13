
async function incarcaStatistici(){


    const raspuns = await fetch(
        `${API}/statistici`
    );


    const date = await raspuns.json();


    document.getElementById("dashboard").innerHTML = `


    <div class="card">

    <h3>Total candidati</h3>

    <p>${date.total}</p>

    </div>



    <div class="card">

    <h3>High Potential</h3>

    <p>${date.high_potential}</p>

    </div>



    <div class="card">

    <h3>Procent High Potential</h3>

    <p>${date.procent_high_potential}%</p>

    </div>



    <div class="card">

    <h3>Scor mediu</h3>

    <p>${date.medie_scor}/100</p>

    </div>

    <div class="card">

    <h3>Performanta medie</h3>

    <p>${date.medie_performanta}/10</p>

    </div>

    `;
    if(window.nivelChartInstance){

    window.nivelChartInstance.destroy();

    }



    window.nivelChartInstance = new Chart(

    document.getElementById("nivelChart"),

    {

    type:"bar",

    data:{

    labels:[

    "High Potential",
    "Ready Soon",
    "Developing",
    "Needs Improvement"

    ],


    datasets:[{

    label:"Numar candidati",

    data:[

    date.high_potential,
    date.ready_soon,
    date.developing,
    date.needs_improvement

    ],

    borderWidth:1

    }]

    },


    options:{

    responsive:true,

    maintainAspectRatio:false,

    scales:{

    y:{

    beginAtZero:true

    }

    }

    }

    }

    );
}


async function incarcaCandidati() {

    if(document.querySelector(".profil")){
        console.log("STOP - sunt deja in profil");
        return;
    }

    console.trace("!!! INCARCA CANDIDATI A FOST APELATA");

    try {

        const raspuns = await fetch(
            `${API}/candidati`
        );


        const candidati = await raspuns.json();
        listaCompleta = candidati;


        afiseazaCandidati(candidati);


    } catch (eroare) {

        console.log("Eroare conectare:", eroare);

        document.getElementById("lista").innerHTML =
            "Nu se poate conecta la server.";

    }

}



function afiseazaCandidati(candidati) {


    let tabel = `

        <table>

            <tr>
                <th>Nume</th>
                <th>Experienta</th>
                <th>Performanta</th>
                <th>Certificari</th>
                <th>Scor</th>
                <th>Nivel</th>
            </tr>

    `;



    candidati.forEach(candidat => {


        tabel += `

            <tr onclick="veziProfil('${candidat.nume}')">

                <td>
                ${candidat.nume}
                </td>


                <td>
                ${candidat.experienta} ani
                </td>


                <td>

                <div class="progress">

                <div class="progress-bar"
                style="width:${candidat.performanta*10}%">

                </div>

                </div>

                ${candidat.performanta}/10

                </td>


                <td>

                ${candidat.certificari}

                </td>

                <td>${candidat.scor}/100</td>

                <td>

                <span class="nivel ${candidat.nivel.replace(/\s/g,'-')}">

                ${candidat.nivel}

                </span>

                </td>

            </tr>

        `;


    });



    tabel += "</table>";



    document.getElementById("lista").innerHTML = tabel;

}

async function adaugaCandidat(){

    const nume = document.getElementById("nume").value;

    if(nume.trim() === ""){

        alert("Introdu numele candidatului!");

        return;
    }


    const experienta = Number(
    document.getElementById("experienta").value
    );
    if (
        document.getElementById("experienta").value.trim() === "" ||
        document.getElementById("performanta").value.trim() === "" ||
        document.getElementById("certificari").value.trim() === ""
    ) {
        alert("Completeaza toate campurile!");
        return;
    }

    const performanta = Number(
        document.getElementById("performanta").value
    );

    const certificari = Number(
        document.getElementById("certificari").value
    );

    if(experienta < 0){

        alert("Experienta nu poate fi negativa!");

        return;
    }

    if(performanta < 0 || performanta > 10){

        alert("Performanta trebuie intre 0 si 10!");

        return;
    }

    if(certificari < 0){

        alert("Certificarile nu pot fi negative!");

        return;
    }


    const candidat = {

    nume: nume,

    experienta: experienta,

    performanta: performanta,

    certificari: certificari

};


    await fetch(
    `${API}/candidati`,
        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(candidat)

        }
    );


    alert("Candidat adaugat!");

    incarcaStatistici();

    incarcaCandidati();

    document.getElementById("nume").value = "";
    document.getElementById("experienta").value = "";
    document.getElementById("performanta").value = "";
    document.getElementById("certificari").value = "";

}

async function veziProfil(nume){


    const raspuns = await fetch(
        `${API}/candidati/${nume}`
    );


    const candidat = await raspuns.json();


    afiseazaProfil(candidat);

}


async function afiseazaProfil(candidat){


    const raspuns = await fetch(
        `${API}/evaluare/${candidat.nume}`
    );


    const evaluare = await raspuns.json();


    const raspunsIstoric = await fetch(
    `${API}/istoric/${candidat.nume}`
    );


    const istoric = await raspunsIstoric.json();

    const raspunsComentarii = await fetch(
    `${API}/comentarii/${candidat.nume}`
    );


    const comentarii = await raspunsComentarii.json();


    // Sorteaza istoric dupa data (crescator) si defineste ultimaEvaluare
    istoric.sort((a, b) => new Date(a.data) - new Date(b.data));

    const ultimaEvaluare = istoric.length > 0 ? istoric[istoric.length - 1] : null;


    const raspunsAnaliza = await fetch(
        `${API}/analiza/${candidat.nume}`
    );


    const analiza = await raspunsAnaliza.json();


    document.getElementById("lista").innerHTML = `


        <div class="profil">


            <h2>${candidat.nume}</h2>
            <h2>

    ${candidat.nume}

    </h2>


    <h2>

    <span class="nivel ${evaluare.nivel.replace(/\s/g,'-')}">

    ${evaluare.nivel}

    </span>

    </h2>

            <hr>


            <h3>Date candidat</h3>


            <p>
            Experienta:
            ${candidat.experienta} ani
            </p>


            <p>
            Performanta:
            ${candidat.performanta}/10
            </p>


            <p>
            Certificari:
            ${candidat.certificari}
            </p>


            <hr>


            <h3>Evaluare</h3>


            <p>
            Scor:
            ${evaluare.scor}/100
            </p>


            <p>

            Nivel:

            <span class="nivel ${evaluare.nivel.replace(/\s/g,'-')}">

            ${evaluare.nivel}

            </span>

            </p>

            <p>
            Recomandare:
            ${evaluare.recomandare}
            </p>

            <p>
            Ultima evaluare:
            ${ultimaEvaluare ? ultimaEvaluare.data : "Niciodata"}
            </p>

            <p>
            Total evaluari:
            ${istoric.length}
            </p>


        <h3>Evaluare manuala</h3>

        <input id="evalExp" placeholder="Experienta">

        <input id="evalPerf" placeholder="Performanta">

        <input id="evalCert" placeholder="Certificari">


        <button type="button" onclick="reevalueaza('${candidat.nume}')">
        Evalueaza acum
        </button>


        <h3>Analiza evolutie</h3>


<p>
Primul scor:
${analiza.primul_scor || 0}
</p>


<p>
Ultimul scor:
${analiza.ultimul_scor || 0}
</p>


<p>
Diferenta:
${analiza.diferenta || 0}
puncte
</p>


<p>

Trend:

<span class="${
analiza.trend==="Pozitiv"

?

"trendPozitiv"

:

analiza.trend==="Negativ"

?

"trendNegativ"

:

"trendStabil"

}">

${analiza.trend}

</span>

</p>

<h3>Comentarii HR</h3>


${comentarii.map(c => `

<p>
${c.comentariu}
</p>

<hr>

`).join("")}


<textarea 
id="comentariuNou"
placeholder="Adauga nota HR">
</textarea>


<br>


<button onclick="salveazaComentariu('${candidat.nume}')">

Salveaza comentariu

</button>

<h3>Istoric evaluari</h3>

<div class="chart-container">
    <canvas id="evolutieChart"></canvas>
</div>


${istoric.map(e => `

<p>

${e.data || ""}

<br>

Scor:
${e.scor}

<br>

Nivel:
${e.nivel}

</p>

<hr>

`).join("")}


            <button type="button" onclick="incarcaStatistici(); incarcaCandidati();">
            Inapoi
            </button>


            <button type="button" onclick="editeazaCandidat('${candidat.nume}')">
            Editeaza
            </button>


            <button type="button" onclick="descarcaRaportPDF('${candidat.nume}')">
            📄 Descarcă raport PDF
            </button>


            <button type="button" onclick="stergeCandidat('${candidat.nume}')">
            Sterge
            </button>


        </div>


        `;

        if (istoric.length > 0) {

        const scoruri = istoric.map(e => e.scor);

        const date = istoric.map(e => e.data || "Evaluare");

        if (window.evolutieChartInstance) {
            window.evolutieChartInstance.destroy();
        }

        window.evolutieChartInstance = new Chart(

            document.getElementById("evolutieChart"),

            {

                type: "line",

                data: {

                    labels: date,

                    datasets: [

                        {

                            label: "Evolutie scor",

                            data: scoruri,

                            borderWidth: 3,

                            tension: 0.3,

                            fill: false

                        }

                    ]

                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    scales: {

                        y: {

                            beginAtZero: true,

                            max: 100

                        }

                    }

                }

            }

        );

    }
}

async function stergeCandidat(nume){


    let confirmare = confirm(
        "Sigur vrei sa stergi candidatul?"
    );


    if(!confirmare){

        return;

    }


    await fetch(
        `${API}/candidati/${nume}`,
        {
            method:"DELETE"
        }
    );


    alert("Candidat sters");

    incarcaStatistici();

    incarcaCandidati();

}

async function editeazaCandidat(nume){


    let experienta = prompt(
        "Experienta noua:"
    );


    let performanta = prompt(
        "Performanta noua:"
    );


    let certificari = prompt(
        "Certificari noi:"
    );



    const date = {

        experienta:Number(experienta),

        performanta:Number(performanta),

        certificari:Number(certificari)

    };

    if(date.experienta < 0){

    alert("Experienta invalida");

    return;

    }

    if(date.performanta < 0 || date.performanta > 10){

        alert("Performanta trebuie intre 0 si 10");

        return;

    }

    if(date.certificari < 0){

        alert("Certificari invalide");

        return;

    }

    let confirmare = confirm(
    "Salvezi modificarile?"
    );

    if(!confirmare){

        return;
    }


    await fetch(

        `${API}/candidati/${nume}`,

        {

            method:"PUT",

            headers:{
                "Content-Type":"application/json"
            },


            body:JSON.stringify(date)

        }

    );


    alert(
        "Candidat actualizat"
    );


    incarcaStatistici();
    incarcaCandidati();
}

let listaCompleta = [];


async function cautaCandidat(){


    let text = document
    .getElementById("cautare")
    .value
    .toLowerCase();



    let filtrati = listaCompleta.filter(c =>

        c.nume.toLowerCase()
        .includes(text)

    );


    afiseazaCandidati(filtrati);

}

function filtreazaNivel(){


    const nivel =
    document.getElementById("filtru").value;



    if(nivel === "toate"){

        afiseazaCandidati(listaCompleta);

        return;

    }


    const filtrati = listaCompleta.filter(candidat => {

        return candidat.nivel === nivel;

    });


    afiseazaCandidati(filtrati);

}


async function reevalueaza(nume){

    console.log("AM INTRAT IN REEVALUARE");

    const date = {

        experienta:Number(
            document.getElementById("evalExp").value
        ),

        performanta:Number(
            document.getElementById("evalPerf").value
        ),

        certificari:Number(
            document.getElementById("evalCert").value
        )

    };


    if(date.experienta < 0){

        alert("Experienta invalida");

        return;

    }


    if(date.performanta < 0 || date.performanta > 10){

        alert("Performanta trebuie intre 0 si 10");

        return;

    }


    if(date.certificari < 0){

        alert("Certificari invalide");

        return;

    }


    let confirmare = confirm(
        "Esti sigur ca doresti o noua evaluare?"
    );


    if(!confirmare){

        return;

    }

    console.log("TRIMIT EVALUAREA");

    const raspuns = await fetch(

        `${API}/reevaluare/${nume}`,

        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify(date)

        }

    );


    const rezultat = await raspuns.json();


    alert(
        "Evaluare noua: " + rezultat.scor
    );



    const raspunsProfil = await fetch(

        `${API}/candidati/${nume}`

    );


    const candidatActualizat = await raspunsProfil.json();



    console.log("INAINTE PROFIL");

    console.log("REINCARCARE PROFIL DUPA EVALUARE");

    await afiseazaProfil(candidatActualizat);


}

async function salveazaComentariu(nume){


    const text =
    document.getElementById("comentariuNou").value;


    if(text.trim() === ""){

        alert("Scrie un comentariu!");

        return;

    }


    await fetch(

        `${API}/comentarii/${nume}`,

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"

            },

            body:JSON.stringify({

                comentariu:text

            })

        }

    );


    alert("Comentariu salvat");

    veziProfil(nume);

}

window.addEventListener("DOMContentLoaded", () => {

    if(document.getElementById("dashboard")){

        incarcaStatistici();

        incarcaCandidati();

    }

});

function descarcaRaportPDF(nume){


    window.open(
        `${API}/raport_pdf/${nume}`,
        "_blank"
    );


}

function logout(){


    localStorage.clear();


    window.location="login.html";
}
