# Display the normal vectors of the sample in the 3D visualisation
gvxr.displayNormalVectors(True)

# Show the 3D objects in wireframe mode
gvxr.useWireframe(True)

# Do not show the beam
gvxr.displayBeam(False)

# Update the visualisation
gvxr.displayScene()

# Take a screenshot
screenshot = gvxr.takeScreenshot();
# Display it using Matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(screenshot)
plt.title("Screenshot of the X-ray simulation environment")
plt.axis('off')
plt.show()