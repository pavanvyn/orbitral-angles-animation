import numpy as np
import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

def rotation_matrix(o,i,w): # LANs, incs and APs repectively - same as Euler angles
    # COUNTER-CLOCKWISE ROTATION
    x1, x2, x3 = np.cos(o)*np.cos(w) - np.sin(o)*np.cos(i)*np.sin(w), \
                np.sin(o)*np.cos(w) + np.cos(o)*np.cos(i)*np.sin(w), \
                np.sin(i)*np.sin(w)
    y1, y2, y3 = np.cos(o)*np.sin(w) + np.sin(o)*np.cos(i)*np.cos(w), \
                np.sin(o)*np.sin(w) - np.cos(o)*np.cos(i)*np.cos(w), \
                - np.sin(i)*np.cos(w)
    z1, z2, z3 = np.sin(o)*np.sin(i), \
                - np.cos(o)*np.sin(i), \
                np.cos(i)
    
    R = np.array([[x1,x2,x3],[y1,y2,y3],[z1,z2,z3]])
    return R

plt.style.use('dark_background')

fig = plt.figure(figsize=(20,6),constrained_layout=True)
ax1 = fig.add_subplot(131,projection='3d')
ax2 = fig.add_subplot(132,projection='3d')
ax3 = fig.add_subplot(133,projection='3d')
for ax in [ax1,ax2,ax3]:
    ax.set_axis_off()
    # ax.grid(None)
    # ax.w_xaxis.pane.fill = False
    # ax.w_yaxis.pane.fill = False
    # ax.w_zaxis.pane.fill = False

p = np.linspace(0.0,359.0,360) # parameter array (for the plotting of the ellipse)
a, b = 1.5, 1 # semi-major and semi-minor axes values
Ell_0 = np.array([a*np.cos(p*np.pi/180.0), b*np.sin(p*np.pi/180.0), np.zeros(len(p))]) # initial ellipse
ax1.plot(Ell_0[0,:],Ell_0[1,:],Ell_0[2,:],lw=1,color='#888888')[0]
ax2.plot(Ell_0[0,:],Ell_0[1,:],Ell_0[2,:],lw=1,color='#888888')[0]
ax3.plot(Ell_0[0,:],Ell_0[1,:],Ell_0[2,:],lw=1,color='#888888')[0]

p_normal = np.linspace(0.0,1.0,2) # parameter array (for the plotting of the normal)
ax1.plot(np.zeros(2),np.zeros(2),p_normal,lw=1,linestyle='dashed',color='#888888')[0]
ax2.plot(np.zeros(2),np.zeros(2),p_normal,lw=1,linestyle='dashed',color='#888888')[0]
ax3.plot(np.zeros(2),np.zeros(2),p_normal,lw=1,linestyle='dashed',color='#888888')[0]

p_node = np.linspace(-1.0,1.0,2) # parameter array (for the plotting of the node line)

orbit1 = ax1.plot([],[],[],lw=2,color='#ffffff')[0]
orbit2 = ax2.plot([],[],[],lw=2,color='#ffffff')[0]
orbit3 = ax3.plot([],[],[],lw=2,color='#ffffff')[0]
orbit = [orbit1, orbit2, orbit3]

normal1 = ax1.plot([],[],[],lw=2,linestyle='dashed',color='#ffffff')[0]
normal2 = ax2.plot([],[],[],lw=2,linestyle='dashed',color='#ffffff')[0]
normal3 = ax3.plot([],[],[],lw=2,linestyle='dashed',color='#ffffff')[0]
normal = [normal1, normal2, normal3]

nodeline1 = ax1.plot([],[],[],lw=2,linestyle='dotted',color='#ffffff')[0]
nodeline2 = ax2.plot([],[],[],lw=2,linestyle='dotted',color='#ffffff')[0]
nodeline3 = ax3.plot([],[],[],lw=2,linestyle='dotted',color='#ffffff')[0]
nodeline = [nodeline1, nodeline2, nodeline3]

ax1.set_title('$\Omega = $ 0 $ ^{\circ}$',fontsize=25)
ax2.set_title('$i = $ 0 $ ^{\circ}$',fontsize=25)
ax3.set_title('$\omega = $ 0 $ ^{\circ}$',fontsize=25)

# function to update matplotlib plot for each frame
def animate(t_step,orbit1,Ell_0,normal,nodeline,t,p,p_normal):
    orbit1, orbit2, orbit3 = orbit
    normal1, normal2, normal3 = normal

    o, i, w = np.pi/4, np.pi/6, np.pi/3 # default (constant) values for LAN, inc and AP

    R1 = rotation_matrix(t[t_step]*np.pi/180.0, i, w) # changing LANs
    R2 = rotation_matrix(o, t[t_step]*np.pi/180.0, w) # changing incs
    R3 = rotation_matrix(o, i, t[t_step]*np.pi/180.0) # changing APs
    Ell_rot1 = np.zeros((3,len(p)))
    Ell_rot2 = np.zeros((3,len(p)))
    Ell_rot3 = np.zeros((3,len(p)))
    for p_i in range(360):
        Ell_rot1[:,p_i] = np.dot(R1.T,Ell_0[:,p_i])
        Ell_rot2[:,p_i] = np.dot(R2.T,Ell_0[:,p_i])
        Ell_rot3[:,p_i] = np.dot(R3.T,Ell_0[:,p_i])
        norm_vec1 = np.dot(R1.T,np.array([0.0,0.0,1.0]))
        norm_vec2 = np.dot(R2.T,np.array([0.0,0.0,1.0]))
        norm_vec3 = np.dot(R3.T,np.array([0.0,0.0,1.0]))

    orbit1.set_data(Ell_rot1[0,:],Ell_rot1[1,:]) # X and Y axes
    orbit1.set_3d_properties(Ell_rot1[2,:]) # Z axis
    orbit2.set_data(Ell_rot2[0,:],Ell_rot2[1,:]) # X and Y axes
    orbit2.set_3d_properties(Ell_rot2[2,:]) # Z axis
    orbit3.set_data(Ell_rot3[0,:],Ell_rot3[1,:]) # X and Y axes
    orbit3.set_3d_properties(Ell_rot3[2,:]) # Z axis

    normal1.set_data(norm_vec1[0]*p_normal,norm_vec1[1]*p_normal)
    normal1.set_3d_properties(norm_vec1[2]*p_normal)
    normal2.set_data(norm_vec2[0]*p_normal,norm_vec2[1]*p_normal)
    normal2.set_3d_properties(norm_vec2[2]*p_normal)
    normal3.set_data(norm_vec3[0]*p_normal,norm_vec3[1]*p_normal)
    normal3.set_3d_properties(norm_vec3[2]*p_normal)

    nodeline1.set_data(np.cos(t[t_step]*np.pi/180.0)*p_node,np.sin(t[t_step]*np.pi/180.0)*p_node)
    nodeline1.set_3d_properties(0*p_node)
    nodeline2.set_data(np.cos(o)*p_node,np.sin(o)*p_node)
    nodeline2.set_3d_properties(0*p_node)
    nodeline3.set_data(np.cos(o)*p_node,np.sin(o)*p_node)
    nodeline3.set_3d_properties(0*p_node)

    ax1.set_title('$\Omega = $ %.0f $ ^{\circ}$'%(t[t_step]),fontsize=25)
    ax2.set_title('$i = $ %.0f $ ^{\circ}$'%(t[t_step]),fontsize=25)
    ax3.set_title('$\omega = $ %.0f $ ^{\circ}$'%(t[t_step]),fontsize=25)

t = np.linspace(0.0,359.0,360) # time array (for changing orbital angles between 0 and 360)
# animate N_steps frames with interval 1ms between frames
anim = animation.FuncAnimation(fig, animate, frames=len(t), fargs=(orbit,Ell_0,normal,nodeline,t,p,p_normal), interval=1, blit=False)

for ax in [ax1,ax2,ax3]:
    # ax.view_init(azim=0, elev=90)
    ax.set_xlim3d([-1.5,1.5])
    ax.set_xlabel('X',fontsize=15)
    ax.set_ylim3d([-1.5,1.5])
    ax.set_ylabel('Y',fontsize=15)
    ax.set_zlim3d([-1.5,1.5])
    ax.set_zlabel('Z',fontsize=15)

plt.show()
anim.save('./orbit_elem.gif',fps=50)