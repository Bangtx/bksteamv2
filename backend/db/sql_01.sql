DROP TABLE IF EXISTS student CASCADE;
CREATE TABLE student
(
  id bigserial NOT NULL,
  name text,
  gender text,
  date_of_birth date,
  password text,
  mail text,
  phone text,
  status int,
  classrooms bigint[],
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_student PRIMARY KEY (id)
);

DROP TABLE IF EXISTS teacher CASCADE;
CREATE TABLE teacher
(
  id bigserial NOT NULL,
  name text,
  gender text,
  date_of_birth date,
  password text,
  mail text,
  phone text,
  classrooms bigint[],
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_teacher PRIMARY KEY (id)
);

DROP TABLE IF EXISTS classroom CASCADE;
CREATE TABLE classroom
(
  id bigserial NOT NULL,
  name text,
  room text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_classroom PRIMARY KEY (id)
);

DROP TABLE IF EXISTS roll_call CASCADE;
CREATE TABLE roll_call
(
  id bigserial NOT NULL,
  date date,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  absent_type int, -- ('Đúng giờ'), ('Nghỉ có phép'), ('Nghỉ không phép'), ('Muộn có phép'), ('Muộn không phép')
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_roll_call PRIMARY KEY (id)
);

DROP TABLE IF EXISTS notification CASCADE;
CREATE TABLE notification
(
  id bigserial NOT NULL,
  date date,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  notification text,
  type text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_notification PRIMARY KEY (id)
);

DROP TABLE IF EXISTS slide CASCADE;
CREATE TABLE slide
(
  id bigserial NOT NULL,
  title text,
  classroom bigint,
  remark text,
  url text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_slide PRIMARY KEY (id)
);

DROP TABLE IF EXISTS unit CASCADE;
CREATE TABLE unit
(
  id bigserial NOT NULL,
  classroom_id bigint,
  title text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_schedule PRIMARY KEY (id)
);

DROP TABLE IF EXISTS score CASCADE;
CREATE TABLE score
(
  id bigserial NOT NULL,
  date date,
  classroom_id bigint,
  student_id bigint,
  teacher_id bigint,
  specking int,
  reading int,
  writing int,
  listening int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_score PRIMARY KEY (id)
);

DROP TABLE IF EXISTS home_work CASCADE;
CREATE TABLE home_work
(
  id bigserial NOT NULL,
  date date,
  deadline date,
  classroom_id bigint,
  unit_id bigint,
  audio bigint,
  multi_choice bool default false, -- 0(multichoice) or 1
  question text,
  option_1 text,
  option_2 text,
  option_3 text,
  option_4 text,
  answers text,
  have_to_do bool default false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work PRIMARY KEY (id)
);

DROP TABLE IF EXISTS home_work_result CASCADE;
CREATE TABLE home_work_result
(
  id bigserial NOT NULL,
  home_work_id bigint,
  student_id bigint,
  answer text,
  is_correct bool default false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work_result PRIMARY KEY (id)
);

DROP TABLE IF EXISTS home_work_file CASCADE;
CREATE TABLE home_work_file
(
  id bigserial NOT NULL,
  date date,
  deadline date,
  classroom_id bigint,
  description text,
  unit_id bigint,
  file_url text,
  is_global bool default true,
  student_ids bigint[],
  have_to_do bool default false,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work_file PRIMARY KEY (id)
);


DROP TABLE IF EXISTS home_work_file_result CASCADE;
CREATE TABLE home_work_file_result
(
  id bigserial NOT NULL,
  home_work_file_id bigint,
  student_id bigint,
  file_result_url text,
  score float,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_home_work_file_result PRIMARY KEY (id)
);

DROP TABLE IF EXISTS self_learning CASCADE;
CREATE TABLE self_learning
(
  id bigserial NOT NULL,
  date date,
  student_id bigint,
  classroom_id bigint,
  absent_type int,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_self_learning PRIMARY KEY (id)
);

DROP TABLE IF EXISTS audio CASCADE;
CREATE TABLE audio
(
  id bigserial NOT NULL,
  url text,
  path text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_audio PRIMARY KEY (id)
);

DROP TABLE IF EXISTS image CASCADE;
CREATE TABLE image
(
  id bigserial NOT NULL,
  url text,
  path text,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  created_by bigint,
  modified_at timestamp with time zone,
  modified_by bigint,
  deleted_at timestamp with time zone,
  deleted_by bigint,
  active boolean DEFAULT TRUE,
  CONSTRAINT pkey_image PRIMARY KEY (id)
);


