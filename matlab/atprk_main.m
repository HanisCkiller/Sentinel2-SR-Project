function atprk_main(mode, input_path, output_path)
    

    fprintf('Running ATPRK...\n');
    fprintf('Mode: %s\n', mode);
    fprintf('Input: %s\n', input_path);
    fprintf('Output: %s\n', output_path);

    addpath(genpath(fileparts(mfilename('fullpath'))));

    try
        switch lower(mode)
            case 'ms'
                fprintf('Running ATPRK_MSsharpen...\n');
                ATPRK_MSsharpen(input_path, output_path);

            case 'pan'
                fprintf('Running ATPRK_PANsharpen...\n');
                ATPRK_PANsharpen(input_path, output_path);

            otherwise
                error('Unknown mode: %s. Use "ms" or "pan".', mode);
        end

        fprintf('ATPRK process completed successfully.\n');

    catch ME
        fprintf(2, 'Error occurred: %s\n', ME.message);
        rethrow(ME);
    end
end