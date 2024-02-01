import maya.cmds as cmds


def create_ui(window_name):
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)

    window = cmds.window(window_name, title="Frame Layout Example")
    
    # resize based on the child components
    main_layout = cmds.scrollLayout(childResizable=True,parent=window)
    main_column_layout = cmds.columnLayout(adjustableColumn=True, parent=main_layout)
    
    colors_frame_layout = cmds.frameLayout(label="Colors",collapsable=True, parent=main_column_layout)
    colors_column_layout = cmds.columnLayout(adjustableColumn=True, parent=colors_frame_layout)
    
    cmds.button("RED",parent=colors_column_layout)
    cmds.button("GREEN",parent=colors_column_layout)
    cmds.button("BLUE",parent=colors_column_layout)
        
    
    numbers_frame_layout = cmds.frameLayout(label="Numbers",collapsable=True, parent=main_column_layout)
    numbers_column_layout = cmds.columnLayout(adjustableColumn=True, parent=numbers_frame_layout)
    
    cmds.button("one",parent=numbers_column_layout)
    cmds.button("two",parent=numbers_column_layout)
    cmds.button("three",parent=numbers_column_layout)


    
    cmds.showWindow(window)


if __name__ == "__main__":
    create_ui("LayoutExampleUI")
