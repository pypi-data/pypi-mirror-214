import numpy as np
import biorbd
import bioviz
from bioviz.biorbd_vtk import VtkModel, Mesh
import genepierre.utils.polytope_computation as pcomp

def visualiseModelPolytopes(model: biorbd.Model, body_name, end_effector: list):
    # Animate the results if biorbd viz is installed
    b = bioviz.Viz(loaded_model=model,background_color=(1,1,1),show_local_ref_frame=False, show_global_ref_frame=False, show_markers=True,show_global_center_of_mass=False,show_segments_center_of_mass=False, show_wrappings=False)
    # define the meshes for the polytope - without robot
    vtkMeshView = VtkModel(b.vtk_window, patch_color=[[0,0.5,0.8]],mesh_opacity=0.5)
    vtkMeshView1 = VtkModel(b.vtk_window, patch_color=[[0,0.5,0.8]],mesh_opacity=0.8, force_wireframe=True)

    b.set_q([0.0,0.3716,-0.5824,1.8218,0.0,0.0,0.0])
    while b.vtk_window.is_active:
        Q = b.Q
        polytope = pcomp.getPolytope(model, Q, body_name, end_effector, tol=1)
        vertices = polytope["vertices"]
        faces = polytope["face_indices"]

        # display polytope in the bioviz
        f_vert_show = np.vstack((vertices[0,:],vertices[1,:],vertices[2,:]))/2000
        f_vert_show = f_vert_show + model.markers(Q)[model.nbMarkers()-1].to_array().reshape(3,1)
        s = f_vert_show.shape
        vert = f_vert_show.reshape(s[0],s[1],1)

        # plot polytope (blue) - with the robot
        meshes = []
        meshes.append(Mesh(vertex=vert, triangles=faces.T))
        vtkMeshView.update_mesh(meshes)
        vtkMeshView1.update_mesh(meshes)

        # update visualisation
        b.update()


def visualiseModelPolytopes_multi(models: list, body_name, end_effector: list, colors=[[0,0.5,0.8], [1,0.5,0.8]]):
    """Visualise first model bu display the 2 polytopes"""
    b = bioviz.Viz(loaded_model=models[0],
                   background_color=(1,1,1),
                   show_local_ref_frame=False, 
                   show_global_ref_frame=False, 
                   show_markers=True,
                   show_global_center_of_mass=False,
                   show_segments_center_of_mass=False, 
                   show_wrappings=False)

    vtkMeshView = VtkModel(b.vtk_window, patch_color=[colors[0]], mesh_opacity=0.5)
    vtkMeshView1 = VtkModel(b.vtk_window, patch_color=[colors[0]], mesh_opacity=0.8, force_wireframe=True)
    
    vtkMeshView2 = VtkModel(b.vtk_window, patch_color=[colors[1]], mesh_opacity=0.5)
    vtkMeshView3 = VtkModel(b.vtk_window, patch_color=[colors[1]], mesh_opacity=0.8, force_wireframe=True)

    b.set_q([0.0,0.3716,-0.5824,1.8218,0.0,0.0,0.0])
    while b.vtk_window.is_active:
        Q = b.Q

        # POLYTOPE 1
        model = models[0]
        polytope = pcomp.getPolytope(model, Q, body_name, end_effector, tol=1)
        vertices = polytope["vertices"]
        faces = polytope["face_indices"]
        f_vert_show = np.vstack((vertices[0,:],vertices[1,:],vertices[2,:]))/2000
        f_vert_show = f_vert_show + model.markers(Q)[model.nbMarkers()-1].to_array().reshape(3,1)
        s = f_vert_show.shape
        vert = f_vert_show.reshape(s[0],s[1],1)

        meshes = []
        meshes.append(Mesh(vertex=vert, triangles=faces.T))
        vtkMeshView.update_mesh(meshes)
        vtkMeshView1.update_mesh(meshes)
        
        # POLYTOPE 2
        model = models[1]
        polytope = pcomp.getPolytope(model, Q, body_name, end_effector, tol=1)
        # print(polytope["error"])
        vertices = polytope["vertices"]
        faces = polytope["face_indices"]
        # print(vertices)
        f_vert_show = np.vstack((vertices[0,:],vertices[1,:],vertices[2,:]))/2000
        f_vert_show = f_vert_show + model.markers(Q)[model.nbMarkers()-1].to_array().reshape(3,1)
        s = f_vert_show.shape
        vert = f_vert_show.reshape(s[0],s[1],1)

        meshes2 = []
        meshes2.append(Mesh(vertex=vert, triangles=faces.T))
        vtkMeshView2.update_mesh(meshes2)
        vtkMeshView3.update_mesh(meshes2)

        # update visualisation
        b.update()


def visualiseModelPolytopesAtQ(model: biorbd.Model, Q: np.ndarray, body_name, end_effector: list):
    # Animate the results if biorbd viz is installed
    b = bioviz.Viz(loaded_model=model,background_color=(1,1,1),show_local_ref_frame=False, show_global_ref_frame=False, show_markers=True,show_global_center_of_mass=False,show_segments_center_of_mass=False, show_wrappings=False)
    # define the meshes for the polytope - without robot
    vtkMeshView = VtkModel(b.vtk_window, patch_color=[[0,0.5,0.8]],mesh_opacity=0.5)
    vtkMeshView1 = VtkModel(b.vtk_window, patch_color=[[0,0.5,0.8]],mesh_opacity=0.8, force_wireframe=True)

    b.set_q(Q.tolist())
    while b.vtk_window.is_active:
        Q = b.Q
        polytope = pcomp.getPolytope(model, Q, body_name, end_effector, tol=1)
        vertices = polytope["vertices"]
        faces = polytope["face_indices"]

        # display polytope in the bioviz
        f_vert_show = np.vstack((vertices[0,:],vertices[1,:],vertices[2,:]))/2000
        f_vert_show = f_vert_show + model.markers(Q)[model.nbMarkers()-1].to_array().reshape(3,1)
        s = f_vert_show.shape
        vert = f_vert_show.reshape(s[0],s[1],1)

        # plot polytope (blue) - with the robot
        meshes = []
        meshes.append(Mesh(vertex=vert, triangles=faces.T))
        vtkMeshView.update_mesh(meshes)
        vtkMeshView1.update_mesh(meshes)

        # update visualisation
        b.update()
    

def visualiseModelAtQNoMarker(model: biorbd.Model, Q: np.ndarray):
    # Animate the results if biorbd viz is installed
    b = bioviz.Viz(loaded_model=model,background_color=(1,1,1),show_local_ref_frame=False, show_global_ref_frame=False, show_markers=False,show_global_center_of_mass=False,show_segments_center_of_mass=False, show_wrappings=False)
    
    b.set_q(Q.tolist())
    while b.vtk_window.is_active:
        Q = b.Q
        b.update()
def visualiseModelAtQ(model: biorbd.Model, Q: np.ndarray):
    # Animate the results if biorbd viz is installed
    b = bioviz.Viz(loaded_model=model,background_color=(1,1,1),show_local_ref_frame=False, show_global_ref_frame=False, show_markers=True,show_global_center_of_mass=False,show_segments_center_of_mass=False, show_wrappings=False)
    
    b.set_q(Q.tolist())
    while b.vtk_window.is_active:
        Q = b.Q
        b.update()