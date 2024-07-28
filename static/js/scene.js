import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.144.0/build/three.module.js';

// Initialize scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(70, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById('xr-canvas'),
    alpha: true,
    antialias: true,
});

// Get the canvas element
const canvas = document.getElementById('xr-canvas');

// Set the renderer size based on the canvas dimensions
renderer.setSize(canvas.clientWidth, canvas.clientHeight);

// Debugging: Log initial setup
console.log('Scene initialized');
console.log(`Canvas Size: ${canvas.clientWidth}x${canvas.clientHeight}`);

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
    videoTexture.format = THREE.RGBAFormat; // Updated to RGBAFormat

    // Debugging: Verify image texture
    console.log('Image texture created:', videoTexture);

    // Create a plane geometry for the video
    const videoGeometry = new THREE.PlaneGeometry(16, 9);
    const videoMaterial = new THREE.MeshBasicMaterial({ map: videoTexture });
    const videoMesh = new THREE.Mesh(videoGeometry, videoMaterial);
    videoMesh.position.z = -5; // Position the plane in front of the camera
    scene.add(videoMesh);

    // Debugging: Log mesh addition
    console.log('Video mesh added to scene');

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);

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
    // Update the aspect ratio based on canvas size
    camera.aspect = canvas.clientWidth / canvas.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    console.log('Window resized');
}
