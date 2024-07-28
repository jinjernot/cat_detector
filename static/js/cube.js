import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.144.0/build/three.module.js';

// Initialize scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById('xr-canvas'),
    alpha: true, // Enable transparency for overlay
    antialias: true, // Enable antialiasing for smoother edges
});

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Debugging: Log initial setup
console.log('Scene initialized');
console.log(`Canvas Size: ${renderer.domElement.width}x${renderer.domElement.height}`);

// Access the img element for the video stream
const videoImg = document.getElementById('video-stream');

// Listen for the image to be loaded
videoImg.onload = function() {
    console.log('Image loaded');

    // Create a texture from the image
    const videoTexture = new THREE.Texture(videoImg);
    videoTexture.needsUpdate = true;
    videoTexture.minFilter = THREE.LinearFilter;
    videoTexture.magFilter = THREE.LinearFilter;
    videoTexture.format = THREE.RGBFormat;

    // Debugging: Verify image texture
    console.log('Image texture created:', videoTexture);

    // Create a plane geometry for the video
    const videoGeometry = new THREE.PlaneGeometry(16, 9);
    const videoMaterial = new THREE.MeshBasicMaterial({ map: videoTexture });
    const videoMesh = new THREE.Mesh(videoGeometry, videoMaterial);
    videoMesh.position.z = -5; // Position the plane in front of the camera
    scene.add(videoMesh);

    // Debugging: Log mesh addition
    console.log('Image mesh added to scene');

    // Create a simple cube
    const cubeGeometry = new THREE.BoxGeometry(1, 1, 1);
    const cubeMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    cube.position.set(0, 0, -3); // Position the cube in front of the camera
    scene.add(cube);

    // Debugging: Log cube addition
    console.log('Cube added to scene');

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

        // Rotate the cube
        cube.rotation.x += 0.01;
        cube.rotation.y += 0.01;

        // Update the video texture to ensure it's refreshed
        videoTexture.needsUpdate = true;

        // Render the scene
        renderer.render(scene, camera);
    }

    // Start the animation loop
    animate();

    // Debugging: Log animation start
    console.log('Animation loop started');
};

// Update renderer and camera on resize
window.addEventListener('resize', onWindowResize, false);
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    console.log('Window resized');
}
