const API = "https://hr-ai-system-by-mihai.onrender.com";

const USER =
localStorage.getItem("user") || "demo";

async function apiFetch(url, options={}){

    options.headers = options.headers || {};

    options.headers["user"] = USER;

    return fetch(url, options);

}


async function incarcaStatistici(){


    const raspuns = await fetch(
        `${API}/statistici`
    );


    const date = await raspuns.json();


    document.getElementById("dashboard").innerHTML = `


    <div class="card">

    <h3>Total Candidates</h3>

    <p>${date.total}</p>

    </div>



    <div class="card">

    <h3>High Potential</h3>

    <p>${date.high_potential}</p>

    </div>



    <div class="card">

    <h3>High Potential Rate</h3>

    <p>${date.procent_high_potential}%</p>

    </div>



    <div class="card">

    <h3>Average Score</h3>

    <p>${date.medie_scor}/100</p>

    </div>

    <div class="card">

    <h3>Average Performance</h3>

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

    label:"Candidates",

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

    console.trace("!!! INCARCA CANDIDATI A FOST APELATA");

    try {

        const raspuns = await fetch(
            `${API}/candidati`
        );


        const candidati = await raspuns.json();
        listaCompleta = candidati;


        afiseazaCandidati(candidati);


    } catch (eroare) {

        console.log("Connection error:", eroare);

        document.getElementById("lista").innerHTML =
            "Unable to connect to the server.";

    }

}



function afiseazaCandidati(candidati) {


    let tabel = `

        <table>

            <tr>
                <th>Name</th>
                <th>Experience</th>
                <th>Performance</th>
                <th>Certifications</th>
                <th>Score</th>
                <th>Level</th>
            </tr>

    `;



    candidati.forEach(candidat => {


        tabel += `

            <tr onclick="veziProfil('${candidat.nume}')">

                <td>
                ${candidat.nume}
                </td>


                <td>
                ${candidat.experienta} years
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

        alert("Please enter the candidate's name!");

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
        alert("Please complete all fields!");
        return;
    }

    const performanta = Number(
        document.getElementById("performanta").value
    );

    const certificari = Number(
        document.getElementById("certificari").value
    );

    if(experienta < 0){

        alert("Experience cannot be negative!");

        return;
    }

    if(performanta < 0 || performanta > 10){

        alert("Performance must be between 0 and 10!");

        return;
    }

    if(certificari < 0){

        alert("Certifications cannot be negative!");

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


    alert("Candidate added successfully!");

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


            <h3>Candidate Information</h3>


            <p>
            Experience:
            ${candidat.experienta} years
            </p>


            <p>
            Performance:
            ${candidat.performanta}/10
            </p>


            <p>
            Certifications:
            ${candidat.certificari}
            </p>


            <hr>


            <h3>Evaluation</h3>


            <p>
            Score:
            ${evaluare.scor}/100
            </p>


            <p>

            Level:

            <span class="nivel ${evaluare.nivel.replace(/\s/g,'-')}">

            ${evaluare.nivel}

            </span>

            </p>

            <p>
            Recommendation:
            ${evaluare.recomandare}
            </p>

            <p>
            Last Evaluation:
            ${ultimaEvaluare ? ultimaEvaluare.data : "Never"}
            </p>

            <p>
            Total Evaluations:
            ${istoric.length}
            </p>


        <h3>Manual Evaluation</h3>

        <input id="evalExp" placeholder="Experience">

        <input id="evalPerf" placeholder="Performance">

        <input id="evalCert" placeholder="Certifications">


        <button type="button" onclick="reevalueaza('${candidat.nume}')">
        Evaluate Now
        </button>


        <h3>Performance Analysis</h3>


<p>
Initial Score:
${analiza.primul_scor || 0}
</p>


<p>
Latest Score:
${analiza.ultimul_scor || 0}
</p>


<p>
Difference:
${analiza.diferenta || 0}
points
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

<h3>HR Notes</h3>


${comentarii.map(c => `

<p>
${c.comentariu}
</p>

<hr>

`).join("")}


<textarea 
id="comentariuNou"
placeholder="Add HR note">
</textarea>


<br>


<button onclick="salveazaComentariu('${candidat.nume}')">

Save Note

</button>

<h3>Evaluation History</h3>

<div class="chart-container">
    <canvas id="evolutieChart"></canvas>
</div>


${istoric.map(e => `

<p>

${e.data || ""}

<br>

Score:
${e.scor}

<br>

Level:
${e.nivel}

</p>

<hr>

`).join("")}


            <button type="button" 
            onclick="incarcaStatistici(); incarcaCandidati();">
            Back
            </button>


            <button type="button" 
            onclick="editeazaCandidat('${candidat.nume}')">
            Edit
            </button>


            <button type="button" 
            onclick="descarcaRaportPDF('${candidat.nume}')">
            📄 Download PDF Report
            </button>


            <button type="button" 
            onclick="stergeCandidat('${candidat.nume}')">
            Delete
            </button>


        </div>


        `;

        if (istoric.length > 0) {

        const scoruri = istoric.map(e => e.scor);

        const date = istoric.map(e => e.data || "Evaluation");

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

                            label: "Score Evolution",

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
        "Are you sure you want to delete this candidate?"
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


    alert("Candidate deleted");

    incarcaStatistici();

    incarcaCandidati();

}

async function editeazaCandidat(nume){


    let experienta = prompt(
        "New experience:"
    );


    let performanta = prompt(
        "New performance:"
    );


    let certificari = prompt(
        "New certifications:"
    );



    const date = {

        experienta:Number(experienta),

        performanta:Number(performanta),

        certificari:Number(certificari)

    };

    if(date.experienta < 0){

    alert("Invalid experience");

    return;

    }

    if(date.performanta < 0 || date.performanta > 10){

        alert("Performance must be between 0 and 10");

        return;

    }

    if(date.certificari < 0){

        alert("Invalid certifications");

        return;

    }

    let confirmare = confirm(
    "Save changes?"
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
        "Candidate updated"
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

    console.log("STARTING RE-EVALUATION");

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

        alert("Invalid experience");

        return;

    }


    if(date.performanta < 0 || date.performanta > 10){

        alert("Performance must be between 0 and 10");

        return;

    }


    if(date.certificari < 0){

        alert("Invalid certifications");

        return;

    }


    let confirmare = confirm(
        "Are you sure you want to perform a new evaluation?"
    );


    if(!confirmare){

        return;

    }

    console.log("SUBMITTING EVALUATION");

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
        "New evaluation score: " + rezultat.scor
    );



    const raspunsProfil = await fetch(

        `${API}/candidati/${nume}`

    );


    const candidatActualizat = await raspunsProfil.json();



    console.log("BEFORE PROFILE");

    console.log("RELOADING PROFILE AFTER EVALUATION");

    await afiseazaProfil(candidatActualizat);


}

async function salveazaComentariu(nume){


    const text =
    document.getElementById("comentariuNou").value;


    if(text.trim() === ""){

        alert("Please write a comment!");

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


    alert("Comment saved");

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
