%{

Configures the correct modules and paths no matter the working directory.

Contributors:
Samuel Landers

%}

function startup()
    thisFile = mfilename('fullpath');

    % Get the project root *relative to this file*
    root = fileparts(thisFile);

    % Add the path of the root and the modules to the interpreter's path
    % Adding the root allows you to run scripts without root always being the working directory
    addpath(root);
    addpath(genpath(fullfile(root,'modules')));

    clear thisFile root
end