### Welcome to the Endless Sky Galaxy Generator!<br>
<br>
This repo generates plugins, containing a new galaxy generated out of the following options:
<ul>
  <li>the center position of the new galaxy</li>
  <li>amount of systems (between 1 and 500)</li>
  <li>amount of landable planets (between 0 and 500)</li>
  <li>amount of races (between 0 and 12)</li>
  <li>a vanilla system for the wormhole link (choose the name)</li>
  <li>number of suns a system can have</li>
  <li>number of non-landable planets a system can have</li>
  <li>number of minables a system can have</li>
  <li>the background galaxy image (4 to choose )</li>
  <li>radius around a star at which new systems get generated</li>
  <li>density of systems/dead arms</li>
  <li>re-tries of system generation to influence galaxy core density</li>
</ul>
Other used features are:
<ul>
  <li>each race is made of a capital planet, neighbouring colony planets, 4 galactica ships and distributed fleets</li>
  <li>cleaned up wordlists (system names, planet names, landing images, planet images, star images)</li>
  <li>zip creation with correct folder structure (ready to play plugin)</li>
</ul>
<br>
To generate such a galaxy, open an issue and choose the galaxy generation template, modify the values inside the issue form, and post the issue. Between 30 seconds and 1 minute later, this readme shows the new generated galaxy, the generated files, a map of the galaxy, and a link to a zip with the complete plugin data.<br>
<br>
The generated plugins don't offer much play-worthy content, but is a great start for your own plugin creation. So feel free to modify and play around with it.<br>
<br>
Why is it not working? In case you change the values beyond max and min values the script stops before generating fatal errors, so try to stay within the mentioned min max. You can always check the actions tab to see at which point the generation stopped and why.<br>
<br>
Have fun!<br>
<br>
<br>
latest 5 generated galaxies:<br>
<table>
  <tr>
    <td width=200>
      name: galaxy<br>
      <br>
      pos: (5000, -5000)<br>
      systems: 300<br>
      planets: 100<br>
      races: 6<br>
      wormhole: Sagittarius A*<br>
      sunmax: 3<br>
      planetmax: 6<br>
      minablemax: 4<br>
      image: messier<br>
      starradius: 100<br>
      density: 5<br>
      tries: 15<br>
    </td>
    <td width=200>
      plugin:<br><a href="https://github.com/zuckung/ES-GalaxyGenerator/releases/download/Latest/galaxy0.zip">galaxy0.zip</a><br>
      <br>
      <br>
      <a href="generated/galaxy0/MapGenSystems.txt">MapGenSystems.txt</a><br>
      <a href="generated/galaxy0/MapGenPlanets.txt">MapGenPlanets.txt</a><br>
      <a href="generated/galaxy0/MapGenStuff.txt">MapGenStuff.txt</a><br>
    </td>
    <td width=300>
      <a href="generated/galaxy0/MapGenMap.jpg"> <img src='generated/galaxy0/miniMapGenMap.jpg' width='300'></a>
    </td>
  </tr>
</table>


<table>
  <tr>
    <td width=200>
      name: Tester<br>
      <br>
      pos: (-10000, -10000)<br>
      systems: 300<br>
      planets: 100<br>
      races: 6<br>
      wormhole: Sol<br>
      sunmax: 3<br>
      planetmax: 5<br>
      minablemax: 3<br>
      image: fornax<br>
      starradius: 100<br>
      density: 5<br>
      tries: 15<br>
    </td>
    <td width=200>
      plugin:<br><a href="https://github.com/zuckung/ES-GalaxyGenerator/releases/download/Latest/Tester0.zip">Tester0.zip</a><br>
      <br>
      <br>
      <a href="generated/Tester0/MapGenSystems.txt">MapGenSystems.txt</a><br>
      <a href="generated/Tester0/MapGenPlanets.txt">MapGenPlanets.txt</a><br>
      <a href="generated/Tester0/MapGenStuff.txt">MapGenStuff.txt</a><br>
    </td>
    <td width=300>
      <a href="generated/Tester0/MapGenMap.jpg"> <img src='generated/Tester0/miniMapGenMap.jpg' width='300'></a>
    </td>
  </tr>
</table>


<table>
  <tr>
    <td width=200>
      name: Sideside<br>
      <br>
      pos: (-100000, -1000000)<br>
      systems: 9<br>
      planets: 7<br>
      races: 2<br>
      wormhole: Sol<br>
      sunmax: 3<br>
      planetmax: 5<br>
      minablemax: 3<br>
      image: sculptor<br>
      starradius: 100<br>
      density: 5<br>
      tries: 15<br>
    </td>
    <td width=200>
      plugin:<br><a href="https://github.com/zuckung/ES-GalaxyGenerator/releases/download/Latest/Sideside0.zip">Sideside0.zip</a><br>
      <br>
      <br>
      <a href="generated/Sideside0/MapGenSystems.txt">MapGenSystems.txt</a><br>
      <a href="generated/Sideside0/MapGenPlanets.txt">MapGenPlanets.txt</a><br>
      <a href="generated/Sideside0/MapGenStuff.txt">MapGenStuff.txt</a><br>
    </td>
    <td width=300>
      <a href="generated/Sideside0/MapGenMap.jpg"> <img src='generated/Sideside0/miniMapGenMap.jpg' width='300'></a>
    </td>
  </tr>
</table>


<table>
  <tr>
    <td width=200>
      name: Frustrator<br>
      <br>
      pos: (-100000, -100000)<br>
      systems: 500<br>
      planets: 500<br>
      races: 12<br>
      wormhole: Rutilicus<br>
      sunmax: 3<br>
      planetmax: 20<br>
      minablemax: 10<br>
      image: messier<br>
      starradius: 100<br>
      density: 20<br>
      tries: 20<br>
    </td>
    <td width=200>
      plugin:<br><a href="https://github.com/zuckung/ES-GalaxyGenerator/releases/download/Latest/Frustrator0.zip">Frustrator0.zip</a><br>
      <br>
      <br>
      <a href="generated/Frustrator0/MapGenSystems.txt">MapGenSystems.txt</a><br>
      <a href="generated/Frustrator0/MapGenPlanets.txt">MapGenPlanets.txt</a><br>
      <a href="generated/Frustrator0/MapGenStuff.txt">MapGenStuff.txt</a><br>
    </td>
    <td width=300>
      <a href="generated/Frustrator0/MapGenMap.jpg"> <img src='generated/Frustrator0/miniMapGenMap.jpg' width='300'></a>
    </td>
  </tr>
</table>


<table>
  <tr>
    <td width=200>
      name: Doctor Worm<br>
      <br>
      pos: (-3000, -25000)<br>
      systems: 60<br>
      planets: 100<br>
      races: 12<br>
      wormhole: Eta Carinae<br>
      sunmax: 3<br>
      planetmax: 7<br>
      minablemax: 3<br>
      image: sculptor<br>
      starradius: 100<br>
      density: 20<br>
      tries: 15<br>
    </td>
    <td width=200>
      plugin:<br><a href="https://github.com/zuckung/ES-GalaxyGenerator/releases/download/Latest/Doctor Worm0.zip">Doctor Worm0.zip</a><br>
      <br>
      <br>
      <a href="generated/Doctor Worm0/MapGenSystems.txt">MapGenSystems.txt</a><br>
      <a href="generated/Doctor Worm0/MapGenPlanets.txt">MapGenPlanets.txt</a><br>
      <a href="generated/Doctor Worm0/MapGenStuff.txt">MapGenStuff.txt</a><br>
    </td>
    <td width=300>
      <a href="generated/Doctor Worm0/MapGenMap.jpg"> <img src='generated/Doctor Worm0/miniMapGenMap.jpg' width='300'></a>
    </td>
  </tr>
</table>


