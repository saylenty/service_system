Service system
==============
An open service system (quetch or queueing system) simulation with ordered requests (FIFO), constant service time and infinite request waiting time.<br>
<ul>
    <li>Number of channels can be set (default value is 5)</li>
    <li>The requests processing can be suspended and continued (pause/resume)</li>
<ul>
Have a look at the picture below:

<br> ![Schema](./SS.jpg) <br>

__Pay attention__: This is multithread app (it is assumed that you aware of the GIL)